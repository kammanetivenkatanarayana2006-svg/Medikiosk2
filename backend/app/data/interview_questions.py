"""
Deterministic interview question definitions.
These are development questions, not AI-generated.
"""

INTERVIEW_QUESTIONS = [
    {
        "question_id": "intro_01",
        "section": "introduction",
        "question_type": "open_text",
        "text": {
            "english": "Please describe in your own words what brings you here today.",
            "telugu": "మీరు ఈ రోజు ఇక్కడకు ఎందుకు వచ్చారో మీ స్వంత మాటల్లో వివరించండి.",
            "hindi": "आज आप यहाँ क्यों आए हैं, अपने शब्दों में बताएं।",
        },
        "required": True,
        "order": 1,
    },
    {
        "question_id": "chief_complaint_01",
        "section": "chief_complaint",
        "question_type": "open_text",
        "text": {
            "english": "What is your main health concern or chief complaint?",
            "telugu": "మీ ప్రధాన ఆరోగ్య సమస్య లేదా ప్రధాన ఫిర్యాదు ఏమిటి?",
            "hindi": "आपकी मुख्य स्वास्थ्य समस्या या मुख्य शिकायत क्या है?",
        },
        "required": True,
        "order": 2,
    },
    {
        "question_id": "duration_01",
        "section": "duration",
        "question_type": "duration",
        "text": {
            "english": "How long have you been experiencing this problem?",
            "telugu": "మీరు ఈ సమస్యను ఎంతకాలంగా ఎదుర్కొంటున్నారు?",
            "hindi": "आप इस समस्या का सामना कितने समय से कर रहे हैं?",
        },
        "required": True,
        "order": 3,
    },
    {
        "question_id": "onset_01",
        "section": "onset",
        "question_type": "single_choice",
        "text": {
            "english": "How did your symptoms begin?",
            "telugu": "మీ లక్షణాలు ఎలా ప్రారంభమయ్యాయి?",
            "hindi": "आपके लक्षण कैसे शुरू हुए?",
        },
        "options": {
            "english": ["Suddenly", "Gradually", "After an injury", "After an illness"],
            "telugu": ["అకస్మాత్తుగా", "క్రమంగా", "గాయం తర్వాత", "అనారోగ్యం తర్వాత"],
            "hindi": ["अचानक", "धीरे-धीरे", "चोट के बाद", "बीमारी के बाद"],
        },
        "required": True,
        "order": 4,
    },
    {
        "question_id": "symptoms_01",
        "section": "symptoms",
        "question_type": "open_text",
        "text": {
            "english": "Please describe all the symptoms you are experiencing.",
            "telugu": "మీరు అనుభవిస్తున్న అన్ని లక్షణాలను వివరించండి.",
            "hindi": "कृपया आप जिन सभी लक्षणों का अनुभव कर रहे हैं उनका वर्णन करें।",
        },
        "required": True,
        "order": 5,
    },
    {
        "question_id": "severity_01",
        "section": "severity",
        "question_type": "severity",
        "text": {
            "english": "On a scale of 1-10, how severe is your discomfort?",
            "telugu": "1-10 స్కేల్లో, మీ అసౌకర్యం ఎంత తీవ్రంగా ఉంది?",
            "hindi": "1-10 के पैमाने पर, आपकी परेशानी कितनी गंभीर है?",
        },
        "required": True,
        "order": 6,
    },
    {
        "question_id": "aggravating_01",
        "section": "aggravating_factors",
        "question_type": "open_text",
        "text": {
            "english": "What makes your symptoms worse?",
            "telugu": "మీ లక్షణాలను ఏది మరింత తీవ్రతరం చేస్తుంది?",
            "hindi": "आपके लक्षणों को क्या बदतर बनाता है?",
        },
        "required": False,
        "order": 7,
    },
    {
        "question_id": "relieving_01",
        "section": "relieving_factors",
        "question_type": "open_text",
        "text": {
            "english": "What makes your symptoms better?",
            "telugu": "మీ లక్షణాలను ఏది మెరుగుపరుస్తుంది?",
            "hindi": "आपके लक्षणों को क्या बेहतर बनाता है?",
        },
        "required": False,
        "order": 8,
    },
    {
        "question_id": "medical_history_01",
        "section": "medical_history",
        "question_type": "open_text",
        "text": {
            "english": "Do you have any existing medical conditions? Please list them.",
            "telugu": "మీకు ఏవైనా వైద్య పరిస్థితులు ఉన్నాయా? వాటిని జాబితా చేయండి.",
            "hindi": "क्या आपको कोई मौजूदा चिकित्सा स्थितियाँ हैं? कृपया उन्हें सूचीबद्ध करें।",
        },
        "required": False,
        "order": 9,
    },
    {
        "question_id": "medication_01",
        "section": "medication_history",
        "question_type": "open_text",
        "text": {
            "english": "Are you currently taking any medications? Please list them.",
            "telugu": "మీరు ప్రస్తుతం ఏవైనా మందులు తీసుకుంటున్నారా? వాటిని జాబితా చేయండి.",
            "hindi": "क्या आप वर्तमान में कोई दवाएँ ले रहे हैं? कृपया उन्हें सूचीबद्ध करें।",
        },
        "required": False,
        "order": 10,
    },
    {
        "question_id": "allergies_01",
        "section": "allergies",
        "question_type": "open_text",
        "text": {
            "english": "Do you have any known allergies?",
            "telugu": "మీకు తెలిసిన అలెర్జీలు ఏమైనా ఉన్నాయా?",
            "hindi": "क्या आपको कोई ज्ञात एलर्जी है?",
        },
        "required": False,
        "order": 11,
    },
    {
        "question_id": "family_history_01",
        "section": "family_history",
        "question_type": "open_text",
        "text": {
            "english": "Is there any family history of medical conditions?",
            "telugu": "కుటుంబంలో వైద్య పరిస్థితుల చరిత్ర ఉందా?",
            "hindi": "क्या परिवार में चिकित्सा स्थितियों का कोई इतिहास है?",
        },
        "required": False,
        "order": 12,
    },
    {
        "question_id": "appetite_01",
        "section": "appetite",
        "question_type": "single_choice",
        "text": {
            "english": "How is your appetite?",
            "telugu": "మీ ఆకలి ఎలా ఉంది?",
            "hindi": "आपकी भूख कैसी है?",
        },
        "options": {
            "english": ["Normal", "Decreased", "Increased", "No appetite"],
            "telugu": ["సాధారణం", "తగ్గింది", "పెరిగింది", "ఆకలి లేదు"],
            "hindi": ["सामान्य", "कम हुई", "बढ़ी हुई", "भूख नहीं"],
        },
        "required": False,
        "order": 13,
    },
    {
        "question_id": "bowel_01",
        "section": "bowel_habits",
        "question_type": "open_text",
        "text": {
            "english": "Any changes in your bowel habits?",
            "telugu": "మీ మల విసర్జన అలవాట్లలో ఏవైనా మార్పులు ఉన్నాయా?",
            "hindi": "क्या आपके मल त्याग की आदतों में कोई बदलाव है?",
        },
        "required": False,
        "order": 14,
    },
    {
        "question_id": "sleep_01",
        "section": "sleep",
        "question_type": "open_text",
        "text": {
            "english": "How is your sleep? Any difficulties?",
            "telugu": "మీ నిద్ర ఎలా ఉంది? ఏవైనా ఇబ్బందులు ఉన్నాయా?",
            "hindi": "आपकी नींद कैसी है? कोई कठिनाई?",
        },
        "required": False,
        "order": 15,
    },
    {
        "question_id": "lifestyle_01",
        "section": "lifestyle",
        "question_type": "open_text",
        "text": {
            "english": "Please describe your lifestyle (diet, exercise, smoking, alcohol).",
            "telugu": "మీ జీవనశైలిని వివరించండి (ఆహారం, వ్యాయామం, ధూమపానం, మద్యపానం).",
            "hindi": "कृपया अपनी जीवनशैली का वर्णन करें (आहार, व्यायाम, धूम्रपान, शराब)।",
        },
        "required": False,
        "order": 16,
    },
    {
        "question_id": "additional_01",
        "section": "additional_information",
        "question_type": "open_text",
        "text": {
            "english": "Is there anything else you would like to share about your health?",
            "telugu": "మీ ఆరోగ్యం గురించి మీరు ఇంకా ఏదైనా పంచుకోవాలనుకుంటున్నారా?",
            "hindi": "क्या आप अपने स्वास्थ्य के बारे में कुछ और साझा करना चाहेंगे?",
        },
        "required": False,
        "order": 17,
    },
    {
        "question_id": "completion_01",
        "section": "completion",
        "question_type": "open_text",
        "text": {
            "english": "Thank you. Your information has been collected. Please click Continue to complete.",
            "telugu": "ధన్యవాదాలు. మీ సమాచారం సేకరించబడింది. పూర్తి చేయడానికి Continue నొక్కండి.",
            "hindi": "धन्यवाद। आपकी जानकारी एकत्र कर ली गई है। पूरा करने के लिए Continue दबाएं।",
        },
        "required": True,
        "order": 18,
    },
]

def get_question_by_id(question_id: str):
    """Get question definition by ID."""
    for question in INTERVIEW_QUESTIONS:
        if question["question_id"] == question_id:
            return question
    return None

def get_first_question():
    """Get first question of interview."""
    return INTERVIEW_QUESTIONS[0] if INTERVIEW_QUESTIONS else None

def get_next_question(current_question_id: str):
    """Get next question in sequence."""
    for i, question in enumerate(INTERVIEW_QUESTIONS):
        if question["question_id"] == current_question_id:
            if i + 1 < len(INTERVIEW_QUESTIONS):
                return INTERVIEW_QUESTIONS[i + 1]
    return None

def get_question_text(question: dict, language: str = "english") -> str:
    """Get question text for specific language."""
    text_dict = question.get("text", {})
    return text_dict.get(language, text_dict.get("english", ""))