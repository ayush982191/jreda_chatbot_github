def get_mobile_prompt(language):
    prompts = {
        "English": "Please enter your registered mobile number (10 digits):",
        "Hindi": "कृपया अपना पंजीकृत मोबाइल नंबर दर्ज करें (10 अंक):",
        "Bengali": "অনুগ্রহ করে আপনার নিবন্ধিত মোবাইল নম্বর লিখুন (১০ সংখ্যা):",
        "Santali": "Apna registered mobile number dijiye (10 digit):"
    }

    return prompts.get(language, prompts["English"])