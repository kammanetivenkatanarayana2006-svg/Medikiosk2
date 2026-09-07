import React, { useState, useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import InformationCollectedPanel from "../components/clinical/InformationCollectedPanel";
import Badge from "../components/ui/Badge";
import ProgressIndicator from "../components/ui/ProgressIndicator";

import { interviewService } from "../services/interviews";
import { aiService } from "../services/ai";
import { followUpService } from "../services/followUp";

import styles from "./InterviewPage.module.css";

const InterviewPage = () => {
  const navigate = useNavigate();
  const { interviewId } = useParams();

  const [interview, setInterview] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [progress, setProgress] = useState(0);
  const [response, setResponse] = useState("");

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [aiProcessing, setAiProcessing] = useState(false);

  const [error, setError] = useState(null);
  const [completed, setCompleted] = useState(false);

  const [inputMode, setInputMode] = useState("voice");
  const [voiceText, setVoiceText] = useState("");

  const [aiStatus, setAiStatus] = useState({
    available: false,
    model_available: false,
  });

  const [aiSource, setAiSource] = useState("deterministic");

  // Smart follow-up state
  const [followUpState, setFollowUpState] = useState({
    processing: false,
    shouldFollowUp: false,
    targetField: null,
    question: null,
    source: null,
  });

  const responseRef = useRef(null);

  // --------------------------------------------------
  // AI STATUS
  // --------------------------------------------------

  const checkAIStatus = async () => {
    try {
      const result = await aiService.getAIStatus();

      if (result.success) {
        setAiStatus(result.data);
      }
    } catch (err) {
      console.error("AI status error:", err);
    }
  };

  // --------------------------------------------------
  // LOAD INTERVIEW
  // --------------------------------------------------

  const loadInterview = async () => {
    if (!interviewId) {
      setError("Interview ID is missing.");
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await interviewService.getInterview(interviewId);

      if (result.success) {
        const interviewData = result.data?.interview;
        const questionData = result.data?.current_question;

        setInterview(interviewData || null);
        setCurrentQuestion(questionData || null);
        setProgress(result.data?.progress || 0);

        // Reset follow-up state when loading a normal question
        setFollowUpState({
          processing: false,
          shouldFollowUp: false,
          targetField: null,
          question: null,
          source: null,
        });

        if (interviewData?.status === "completed") {
          setCompleted(true);
        }
      } else {
        setError(result.error || "Failed to load interview.");
      }
    } catch (err) {
      console.error("Load interview error:", err);
      setError("Unable to load interview. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInterview();
    checkAIStatus();
  }, [interviewId]);

  useEffect(() => {
    if (currentQuestion && !loading && inputMode === "text") {
      responseRef.current?.focus();
    }
  }, [currentQuestion, loading, inputMode]);

  // --------------------------------------------------
  // START INTERVIEW
  // --------------------------------------------------

  const handleStart = async () => {
    if (!interviewId) {
      setError("Interview ID is missing.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await interviewService.startInterview(interviewId);

      if (result.success) {
        await loadInterview();
      } else {
        setError(result.error || "Failed to start interview.");
        setLoading(false);
      }
    } catch (err) {
      console.error("Start interview error:", err);
      setError("Unable to start interview. Please try again.");
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // SUBMIT RESPONSE
  // --------------------------------------------------

  const handleSubmit = async () => {
    const trimmedResponse = response.trim();

    if (!trimmedResponse) {
      return;
    }

    if (!currentQuestion?.question_id) {
      setError("Current question is not available.");
      return;
    }

    setSubmitting(true);
    setAiProcessing(true);
    setError(null);

    try {
      // ----------------------------------------------
      // 1. SAVE USER RESPONSE
      // ----------------------------------------------

      const submitResult = await interviewService.submitResponse(
        interviewId,
        currentQuestion.question_id,
        trimmedResponse,
      );

      if (!submitResult.success) {
        setError(submitResult.error || "Failed to submit response.");
        return;
      }

      setResponse("");
      setVoiceText("");

      // ----------------------------------------------
      // 2. CHECK INTERVIEW COMPLETION
      // ----------------------------------------------

      if (submitResult.data?.completed) {
        setCompleted(true);
        setProgress(100);
        return;
      }

      // ----------------------------------------------
      // 3. CHECK SMART FOLLOW-UP
      // ----------------------------------------------

      setFollowUpState((prev) => ({
        ...prev,
        processing: true,
      }));

      try {
        const followUpResult = await followUpService.getFollowUp(
          interviewId,
          submitResult.data?.response_id || "",
        );

        if (
          followUpResult.success &&
          followUpResult.data?.should_follow_up
        ) {
          const followUpQuestion = followUpResult.data.question;

          setFollowUpState({
            processing: false,
            shouldFollowUp: true,
            targetField: followUpResult.data.target_field,
            question: followUpQuestion,
            source: followUpResult.data.source,
          });

          // Show follow-up question
          setCurrentQuestion({
            question_id: `followup_${followUpResult.data.target_field}_${Date.now()}`,
            text: followUpQuestion,
            section: currentQuestion.section,
            question_type: "open_text",
            options: [],
          });

          setAiSource("follow_up");

          // Follow-up question displayed.
          // Do not load next question yet.
          return;
        }

        // No follow-up
        setFollowUpState((prev) => ({
          ...prev,
          processing: false,
          shouldFollowUp: false,
        }));
      } catch (followUpError) {
        console.error("Follow-up error:", followUpError);

        // Follow-up failure should not break interview
        setFollowUpState((prev) => ({
          ...prev,
          processing: false,
          shouldFollowUp: false,
        }));
      }

      // ----------------------------------------------
      // 4. TRY AI-GENERATED NEXT QUESTION
      // ----------------------------------------------

      try {
        const aiResult = await aiService.getNextQuestion(
          interviewId,
          currentQuestion.question_id,
          trimmedResponse,
        );

        if (aiResult.success && aiResult.data?.question) {
          setCurrentQuestion({
            question_id:
              aiResult.data.next_question_id || `ai_${Date.now()}`,
            text: aiResult.data.question,
            section:
              aiResult.data.section || currentQuestion.section,
            question_type: "open_text",
            options: [],
          });

          setAiSource(aiResult.data.source || "ai");

          if (typeof aiResult.data.progress === "number") {
            setProgress(aiResult.data.progress);
          }
        } else {
          // AI failed → deterministic question
          await loadInterview();
          setAiSource("deterministic");
        }
      } catch (aiError) {
        console.error("AI next question error:", aiError);

        // AI failure should not break the interview
        await loadInterview();
        setAiSource("deterministic");
      }
    } catch (err) {
      console.error("Submit response error:", err);
      setError("Unable to submit response. Please try again.");
    } finally {
      setAiProcessing(false);
      setSubmitting(false);
    }
  };

  // --------------------------------------------------
  // PAUSE INTERVIEW
  // --------------------------------------------------

  const handlePause = async () => {
    if (!interviewId) {
      setError("Interview ID is missing.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await interviewService.pauseInterview(interviewId);

      if (result.success) {
        navigate("/patient/home");
      } else {
        setError(result.error || "Failed to pause interview.");
      }
    } catch (err) {
      console.error("Pause interview error:", err);
      setError("Unable to pause interview. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // CANCEL INTERVIEW
  // --------------------------------------------------

  const handleCancel = async () => {
    const confirmed = window.confirm(
      "Are you sure you want to cancel the interview?",
    );

    if (!confirmed) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await interviewService.cancelInterview(interviewId);

      if (result.success) {
        navigate("/patient/home");
      } else {
        setError(result.error || "Failed to cancel interview.");
      }
    } catch (err) {
      console.error("Cancel interview error:", err);
      setError("Unable to cancel interview. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // VOICE / TEXT INPUT
  // --------------------------------------------------

  const handleVoiceTranscription = (text) => {
    setVoiceText(text);
    setResponse(text);
  };

  const handleTextFallback = () => {
    setInputMode("text");
  };

  const handleVoiceMode = () => {
    setInputMode("voice");
  };

  // --------------------------------------------------
  // LOADING SCREEN
  // --------------------------------------------------

  if (loading) {
    return (
      <div className={styles.container}>
        <Card
          variant="glass"
          padding="xlarge"
          className={styles.card}
        >
          <p className={styles.loading}>Loading interview...</p>
        </Card>
      </div>
    );
  }

  // --------------------------------------------------
  // COMPLETED SCREEN
  // --------------------------------------------------

  if (completed) {
    return (
      <div className={styles.container}>
        <Card
          variant="glass"
          padding="xlarge"
          className={styles.card}
        >
          <div className={styles.icon}>✅</div>

          <Badge
            variant="success"
            size="large"
            className={styles.badge}
          >
            Interview Completed
          </Badge>

          <h1 className={`${styles.title} text-h1`}>
            Thank You
          </h1>

          <p className={`${styles.description} text-body-lg`}>
            Your information has been collected and will be prepared
            for healthcare professional review.
          </p>

          <p className={styles.notice}>
            MediKiosk helps organize the information you provide.
            A healthcare professional must review and verify your
            information.
          </p>

          <Button
            variant="primary"
            size="large"
            onClick={() => navigate("/patient/home")}
          >
            RETURN TO HOME
          </Button>
        </Card>
      </div>
    );
  }

  // --------------------------------------------------
  // READY SCREEN
  // --------------------------------------------------

  if (interview?.status === "ready") {
    return (
      <div className={styles.container}>
        <Card
          variant="glass"
          padding="xlarge"
          className={styles.card}
        >
          <h1 className={`${styles.title} text-h1`}>
            Ready to Begin
          </h1>

          <p className={`${styles.subtitle} text-body-lg`}>
            Your clinical interview is ready to start.
          </p>

          <Button
            variant="primary"
            size="xlarge"
            fullWidth
            onClick={handleStart}
          >
            START INTERVIEW
          </Button>
        </Card>
      </div>
    );
  }

  // --------------------------------------------------
  // MAIN INTERVIEW SCREEN
  // --------------------------------------------------

  return (
    <div className={styles.container}>
      <Card
        variant="glass"
        padding="xlarge"
        className={styles.card}
      >
        <div className={styles.header}>
          <Badge variant="primary" size="medium">
            {interview?.language?.toUpperCase() || "ENGLISH"}
          </Badge>

          <Badge variant="default" size="medium">
            {interview?.consultation_type
              ?.replace(/_/g, " ")
              .toUpperCase() || "CONSULTATION"}
          </Badge>
        </div>

        <h1 className={`${styles.title} text-h1`}>
          Clinical Interview
        </h1>

        <div className={styles.section}>
          <span className={styles.sectionLabel}>Section:</span>

          <span className={styles.sectionValue}>
            {currentQuestion?.section
              ?.replace(/_/g, " ")
              .toUpperCase() || "GENERAL"}
          </span>
        </div>

        <ProgressIndicator
          value={progress}
          showValue
          label="Progress"
          className={styles.progress}
        />

        {/* AI SOURCE BADGE */}
        {aiSource === "ai" && (
          <div className={styles.aiBadge}>
            <Badge variant="primary" size="small">
              AI Assisted
            </Badge>
          </div>
        )}

        {/* FOLLOW-UP INDICATOR */}
        {followUpState.shouldFollowUp && (
          <div className={styles.followUpIndicator}>
            <Badge variant="primary" size="small">
              Clarification
            </Badge>
          </div>
        )}

        {/* AI FALLBACK MESSAGE */}
        {!aiStatus.available && (
          <div className={styles.aiFallback}>
            AI assistance unavailable. Using standard interview.
          </div>
        )}

        {/* AI / FOLLOW-UP PROCESSING */}
        {aiProcessing && (
          <div className={styles.aiProcessing}>
            Preparing your next question...
          </div>
        )}

        {/* ERROR */}
        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}

        <InformationCollectedPanel interviewId={interviewId} />

        {/* QUESTION */}
        <div className={styles.questionArea}>
          <p className={styles.questionText}>
            {currentQuestion?.text || "No question available."}
          </p>

          {currentQuestion?.options?.length > 0 && (
            <div className={styles.options}>
              {currentQuestion.options.map((option, index) => (
                <button
                  key={`${option}-${index}`}
                  type="button"
                  className={`${styles.option} ${
                    response === option ? styles.selected : ""
                  }`}
                  onClick={() => setResponse(option)}
                  role="radio"
                  aria-checked={response === option}
                >
                  {option}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* RESPONSE INPUT */}
        <div className={styles.responseArea}>
          {inputMode === "voice" && (
            <div className={styles.voiceArea}>
              <p className={styles.voiceMessage}>
                Voice input mode is selected.
              </p>

              <Button
                variant="outline"
                size="medium"
                onClick={handleTextFallback}
              >
                USE TEXT INPUT
              </Button>
            </div>
          )}

          {inputMode === "text" && (
            <>
              <textarea
                ref={responseRef}
                value={response}
                onChange={(event) =>
                  setResponse(event.target.value)
                }
                placeholder="Enter your response..."
                className={styles.textarea}
                rows={4}
                aria-label="Your response"
              />

              <Button
                variant="ghost"
                size="small"
                onClick={handleVoiceMode}
              >
                USE VOICE INPUT
              </Button>
            </>
          )}
        </div>

        {/* ACTIONS */}
        <div className={styles.actions}>
          <Button
            variant="outline"
            size="large"
            onClick={handlePause}
            disabled={submitting || aiProcessing}
          >
            PAUSE
          </Button>

          <Button
            variant="ghost"
            size="large"
            onClick={handleCancel}
            disabled={submitting || aiProcessing}
          >
            CANCEL
          </Button>

          <Button
            variant="primary"
            size="large"
            onClick={handleSubmit}
            disabled={
              !response.trim() ||
              submitting ||
              aiProcessing
            }
            loading={submitting}
          >
            CONTINUE
          </Button>
        </div>

        <p className={styles.notice}>
          AI-assisted documentation only. A healthcare professional
          must review and verify your information.
        </p>
      </Card>
    </div>
  );
};

export default InterviewPage;