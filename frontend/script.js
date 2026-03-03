// Base URL for API calls. During development this points to the
// locally running Flask server (port 5000). When deployed, you can either
// set this to an absolute URL or rely on Netlify redirects which preserve
// the relative path.
const API_BASE = "https://jreda-chatbot-github.onrender.com";

let currentStep = "language";
let selectedLanguage = null;
let selectedSchema = null;
let grievanceFlow = false;
let issueCollected = false;
let trackMode = false;
let guestMode = false;
let guestName = null;


const LANG = {

    English: {
        yes: "Yes",
        no: "No",
        registeredQuestion: "Are you registered with your mobile number?",
        enterOtp: "Enter OTP (1234):",
        invalidOtp: "Invalid OTP ❌",
        mobileNotRegistered: "Mobile not registered.",
        welcome: (name) => `Hi ${name}, welcome!
You can raise a grievance, track your existing complaint, check scheme details, or view your pump status. `,
        mainMenu: ["Raise Grievance", "Track Grievance", "Details of Schemas", "Device Status"],
        selectSchema: "Select a schema:",
        selectScheme: "Select a scheme:"
    },

    Hindi: {
        yes: "हाँ",
        no: "नहीं",
        registeredQuestion: "क्या आप अपने मोबाइल नंबर से पंजीकृत हैं?",
        enterOtp: "OTP दर्ज करें (1234):",
        invalidOtp: "गलत OTP ❌",
        mobileNotRegistered: "मोबाइल नंबर पंजीकृत नहीं है।",
        welcome: (name) => `नमस्ते ${name}, आपका स्वागत है!
आप शिकायत दर्ज कर सकते हैं, अपनी शिकायत ट्रैक कर सकते हैं, योजना विवरण देख सकते हैं या अपने पंप की स्थिति देख सकते हैं। `,
        mainMenu: ["शिकायत दर्ज करें", "शिकायत ट्रैक करें", "योजनाओं का विवरण", "डिवाइस स्थिति"],
        selectSchema: "एक श्रेणी चुनें:",
        selectScheme: "एक योजना चुनें:"
    },

    Bengali: {
        yes: "হ্যাঁ",
        no: "না",
        registeredQuestion: "আপনি কি আপনার মোবাইল নম্বর দিয়ে নিবন্ধিত?",
        enterOtp: "OTP লিখুন (1234):",
        invalidOtp: "ভুল OTP ❌",
        mobileNotRegistered: "মোবাইল নম্বর নিবন্ধিত নয়।",
        welcome: (name) => `নমস্কার ${name}, আপনাকে স্বাগতম!
আপনি অভিযোগ দাখিল করতে পারেন, অভিযোগ ট্র্যাক করতে পারেন, স্কিমের বিস্তারিত দেখতে পারেন বা পাম্পের অবস্থা দেখতে পারেন। `,
        mainMenu: ["অভিযোগ দাখিল করুন", "অভিযোগ ট্র্যাক করুন", "স্কিমের বিস্তারিত", "ডিভাইস অবস্থা"],
        selectSchema: "একটি বিভাগ নির্বাচন করুন:",
        selectScheme: "একটি স্কিম নির্বাচন করুন:"
    },

    Santali: {
        yes: "Haan",
        no: "Na",
        registeredQuestion: "Apna mobile number se registered achhi?",
        enterOtp: "OTP dijiye (1234):",
        invalidOtp: "Galat OTP ❌",
        mobileNotRegistered: "Mobile number registered nahi hai.",
        welcome: (name) => `Johar ${name}, apnake swagat!
Apni abhijog dakhil kar sakte, abhijog track kar sakte, yojana details dekh sakte ya pump dasa dekh sakte. `,
        mainMenu: ["Abhijog Dakhil", "Abhijog Track", "Yojana Details", "Device Dasa"],
        selectSchema: "Ek category chayan kare:",
        selectScheme: "Ek yojana chayan kare:"
    }
};

const SCHEMES = {
    English: [
        "Solar Pumps",
        "Mini Grids",
        "Rooftop Solar",
        "Solar Water Heater",
        "Solar Street Light",
        "Solar High Mast",
        "PM-KUSUM Scheme (C)",
        "Solar PV Off-Grid Systems",
        "PM JANMAN",
        "Giridih Solar City",
        "Canal-Top Solar Plants"
    ],
    Hindi: [
        "सोलर पंप",
        "मिनी ग्रिड",
        "रूफटॉप सोलर",
        "सोलर वाटर हीटर",
        "सोलर स्ट्रीट लाइट",
        "सोलर हाई मास्ट",
        "पीएम-कुसुम योजना (C)",
        "सोलर पीवी ऑफ-ग्रिड सिस्टम",
        "पीएम जनमन",
        "गिरिडीह सोलर सिटी",
        "कैनाल-टॉप सोलर प्लांट"
    ],
    Bengali: [
        "সোলার পাম্প",
        "মিনি গ্রিড",
        "রুফটপ সোলার",
        "সোলার ওয়াটার হিটার",
        "সোলার স্ট্রিট লাইট",
        "সোলার হাই মাস্ট",
        "পিএম-কুসুম প্রকল্প (C)",
        "সোলার PV অফ-গ্রিড সিস্টেম",
        "পিএম জনমন",
        "গিরিডিহ সোলার সিটি",
        "ক্যানাল-টপ সোলার প্ল্যান্ট"
    ],
    Santali: [
        "Solar Pumps",
        "Mini Grids",
        "Rooftop Solar",
        "Solar Water Heater",
        "Solar Street Light",
        "Solar High Mast",
        "PM-KUSUM Scheme (C)",
        "Solar PV Off-Grid Systems",
        "PM JANMAN",
        "Giridih Solar City",
        "Canal-Top Solar Plants"
    ]
};



/* ================= MESSAGE APPEND ================= */

function appendMessage(msg, cls) {
    let div = document.createElement("div");
    div.className = cls;
    div.innerHTML = msg.replace(/\n/g, "<br>");

    document.getElementById("chat-body").appendChild(div);
    document.getElementById("chat-body").scrollTop =
        document.getElementById("chat-body").scrollHeight;
}

/* ================= AUTO GROW ================= */

function autoGrow(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

/* ================= BUTTON RENDER ================= */

// function appendButtons(buttons, type = "schema") {

//     // Only remove schema buttons, not main menu
//     if (type === "schema") {
//         const oldSchemaButtons = document.querySelectorAll(".schema-buttons");
//         oldSchemaButtons.forEach(btn => btn.remove());
//     }

//     let container = document.createElement("div");

//     if (type === "main") {
//         container.className = "language-buttons";
//     } else {
//         container.className = "schema-buttons";
//     }

//     buttons.forEach(btn => {
//         let button = document.createElement("button");
//         button.className = "dynamic-btn";
//         button.innerText = btn.label;
//         button.onclick = btn.action;
//         container.appendChild(button);
//     });

//     document.getElementById("chat-body").appendChild(container);
// }

function appendButtons(buttons, type = "schema") {

    let container = document.createElement("div");

    if (type === "main") {
        container.className = "language-buttons";
    } else {
        container.className = "schema-buttons";
    }

    buttons.forEach(btn => {
        let button = document.createElement("button");
        button.className = "dynamic-btn";
        button.innerText = btn.label;
        button.onclick = btn.action;
        container.appendChild(button);
    });

    document.getElementById("chat-body").appendChild(container);

    document.getElementById("chat-body").scrollTop =
        document.getElementById("chat-body").scrollHeight;
}

/* ================= LANGUAGE SELECTION ================= */

function selectLanguage(lang, event) {

    selectedLanguage = lang;

    fetch(API_BASE + "/select-language", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language: lang })
    })
    .then(res => res.json())
    .then(data => {

        currentStep = "mobile";

        appendMessage(lang, "user-message");
        appendMessage(LANG[selectedLanguage].registeredQuestion, "bot-message");

        

        appendButtons([
            {
                label: LANG[selectedLanguage].yes,
                action: () => {
                    appendMessage(LANG[selectedLanguage].yes, "user-message");
                    appendMessage(data.message, "bot-message");
                }
            },
            

            {
                label: LANG[selectedLanguage].no,
                action: () => {
                    appendMessage(LANG[selectedLanguage].no, "user-message");

                    guestMode = true;
                    currentStep = "guest_name";

                    appendMessage(
                        selectedLanguage === "Hindi"
                            ? "कृपया अपना नाम दर्ज करें:"
                            : selectedLanguage === "Bengali"
                            ? "অনুগ্রহ করে আপনার নাম লিখুন:"
                            : selectedLanguage === "Santali"
                            ? "Apna nam likhiye:"
                            : "Please enter your name:",
                        "bot-message"
                    );
                }
            }


        ], "main");



        const buttons = document.querySelectorAll(".language-buttons button");
        buttons.forEach(btn => btn.classList.remove("active"));
        event.currentTarget.classList.add("active");
    });
}

/* ================= SEND MESSAGE ================= */

function sendMessage() {

    const input = document.getElementById("user-input");
    const value = input.value.trim();
    if (!value) return;

    appendMessage(value, "user-message");
    input.value = "";
    autoGrow(input);

    // ================= GUEST NAME STEP =================
    if (currentStep === "guest_name") {

        guestName = value;
        currentStep = "guest_mobile";

        appendMessage(
            selectedLanguage === "Hindi"
                ? "कृपया अपना मोबाइल नंबर दर्ज करें:"
                : selectedLanguage === "Bengali"
                ? "অনুগ্রহ করে আপনার মোবাইল নম্বর লিখুন:"
                : selectedLanguage === "Santali"
                ? "Apna mobile number likhiye:"
                : "Please enter your mobile number:",
            "bot-message"
        );

        return;
    }

    // ================= GUEST MOBILE STEP =================
    if (currentStep === "guest_mobile") {

        currentStep = "chat";

        appendMessage(
            selectedLanguage === "Hindi"
                ? `नमस्ते ${guestName}, अब आप JREDA योजनाओं की जानकारी देख सकते हैं।`
                : selectedLanguage === "Bengali"
                ? `নমস্কার ${guestName}, এখন আপনি JREDA স্কিমের তথ্য দেখতে পারেন।`
                : selectedLanguage === "Santali"
                ? `Johar ${guestName}, apni JREDA yojana jankari dekh sakte.`
                : `Hi ${guestName}, now you can explore JREDA scheme information.`,
            "bot-message"
        );

        // 🔥 SHOW ONLY DETAILS OF SCHEMAS
        appendButtons([
            {
                label: LANG[selectedLanguage].mainMenu[2], // Details of Schemas
                action: () => {
                    handleMainMenuClick(LANG[selectedLanguage].mainMenu[2]);
                }
            }
        ], "main");

        return;
    }

    if (currentStep === "mobile") {

        fetch(API_BASE + "/verify-mobile", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mobile: value })
        })
        .then(res => res.json())
        .then(data => {

            if (data.status === "otp_sent") {
                currentStep = "otp";
                appendMessage(LANG[selectedLanguage].enterOtp, "bot-message");
            } else {
                appendMessage(LANG[selectedLanguage].mobileNotRegistered, "bot-message");
            }
        });

        return;
    }

    if (currentStep === "otp") {

        fetch(API_BASE + "/verify-otp", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ otp: value })
        })
        .then(res => res.json())
        .then(data => {


            if (data.status === "success") {

                currentStep = "chat";

                appendMessage(
                    LANG[selectedLanguage].welcome(data.farmer_name),
                    "bot-message"
                );

                showMainMenu();
            } else {
                appendMessage(LANG[selectedLanguage].invalidOtp, "bot-message");
            }
        });
        return;
    }

    
    if (currentStep === "chat") {

        // ✅ Only mark issue once during grievance flow
        if (grievanceFlow && !issueCollected) {
            issueCollected = true;
        }

        showThinking();

        fetch(API_BASE + "/chat", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: value,
                schema: selectedSchema
            })
        })
        .then(res => res.json())
        .then(data => {

            removeThinking();
            appendMessage(data.reply, "bot-message");

            if (data.reply.includes("Grievance ID")) {

                selectedSchema = null;
                grievanceFlow = false;
                issueCollected = false;

                showMainMenu();
            }
        })
        .catch(() => {
            removeThinking();
            appendMessage("Server error ❌", "bot-message");
        });
    }
}

/* ================= MAIN MENU ================= */

function showMainMenu() {

    const labels = LANG[selectedLanguage].mainMenu;

    // 🔥 Add instruction text before buttons
    appendMessage(
        selectedLanguage === "Hindi"
            ? "कृपया नीचे दिए गए विकल्पों में से चुनें:"
            : selectedLanguage === "Bengali"
            ? "নিচের বিকল্পগুলির মধ্যে একটি নির্বাচন করুন:"
            : selectedLanguage === "Santali"
            ? "Niche diya option me se ek chayan kare:"
            : "Please choose one of the following options:",
        "bot-message"
    );

    appendButtons(
        labels.map(label => ({
            label: label,
            action: () => handleMainMenuClick(label)
        })),
        "main"
    );
}

/* ================= HANDLE MAIN MENU CLICK ================= */

function handleMainMenuClick(label) {

    appendMessage(label, "user-message");

    const labels = LANG[selectedLanguage].mainMenu;

    // Index based logic
    if (label === labels[0]) {
        grievanceFlow = true;
        appendMessage(LANG[selectedLanguage].selectSchema || "Select a schema:", "bot-message");
        showSchemaButtons();
        return;
    }

    if (label === labels[1]) {

        showThinking();

        fetch(API_BASE + "/chat", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: "ACTION_TRACK_GRIEVANCE",
                mode: "track"
            })
        })
        .then(res => res.json())
        .then(data => {

            removeThinking();
            appendMessage(data.reply, "bot-message");

            

            showMainMenu();

        })
        .catch(() => {
            removeThinking();
            appendMessage("Server error ❌", "bot-message");
        });

        return;
    }


    if (label === labels[2]) {
        appendMessage(LANG[selectedLanguage].selectScheme || "Select a scheme:", "bot-message");
        showSchemeList();
        return;
    }

    if (label === labels[3]) {
        appendMessage(LANG[selectedLanguage].selectScheme || "Select a scheme:", "bot-message");
        showDeviceSchemeList();
        return;
    }
}



function showSchemeList() {

    const schemes = SCHEMES[selectedLanguage];

    appendButtons(
        schemes.map((s, index) => ({
            label: s,
            action: () => {

                appendMessage(s, "user-message");

                selectedSchema = SCHEMES.English[index];

                showSchemeOptions();
            }
        })),
        "schema"
    );
}

/* ================= DEVICE SCHEME LIST ================= */

function showDeviceSchemeList() {

    const schemes = SCHEMES[selectedLanguage];

    appendButtons(
        schemes.map((s, index) => ({
            label: s,
            action: () => {

                appendMessage(s, "user-message");

                const englishSchema = SCHEMES.English[index];

                if (englishSchema === "PM-KUSUM Scheme (C)") {
                    showPumpStatusButton();
                } else {
                    appendMessage(
                        selectedLanguage === "Hindi"
                            ? "डिवाइस स्थिति डेटा केवल पीएम-कुसुम योजना (C) के लिए उपलब्ध है।"
                            : selectedLanguage === "Bengali"
                            ? "ডিভাইস তথ্য শুধুমাত্র PM-KUSUM স্কিম (C) এর জন্য উপলব্ধ।"
                            : selectedLanguage === "Santali"
                            ? "Device data sirf PM-KUSUM Scheme (C) ke liye uplabdh hai."
                            : "Device status data is currently available only for PM-KUSUM Scheme (C).",
                        "bot-message"
                    );
                }
            }
        })),
        "schema"
    );
}

function sendPumpStatusRequest() {

    showThinking();

    fetch(API_BASE + "/chat", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: "SOLAR_PUMP_STATUS"
        })
    })
    .then(res => res.json())
    .then(data => {

        removeThinking();
        appendMessage(data.reply, "bot-message");

        // ✅ After device response, show main menu again
        showMainMenu();

    })
    .catch(() => {
        removeThinking();
        appendMessage("Server error ❌", "bot-message");
    });
}

/* ================= SOLAR PUMP STATUS BUTTON ================= */

function showPumpStatusButton() {

    const instruction =
        selectedLanguage === "Hindi"
            ? "कृपया नीचे दिया गया विकल्प चुनें:"
            : selectedLanguage === "Bengali"
            ? "অনুগ্রহ করে নিচের বিকল্পটি নির্বাচন করুন:"
            : selectedLanguage === "Santali"
            ? "Niche diya option chayan kare:"
            : "Please choose the following option:";

    const buttonLabel =
        selectedLanguage === "Hindi"
            ? "सोलर पंप स्थिति"
            : selectedLanguage === "Bengali"
            ? "সোলার পাম্প অবস্থা"
            : selectedLanguage === "Santali"
            ? "Solar Pump Dasa"
            : "Solar Pump Status";

    appendMessage(instruction, "bot-message");

    appendButtons([
        {
            label: buttonLabel,
            action: () => {
                appendMessage(buttonLabel, "user-message");
                sendPumpStatusRequest();
            }
        }
    ], "schema");
}



/* ================= SCHEMA LIST ================= */

function showSchemaButtons() {

    const schemas = SCHEMES[selectedLanguage];

    appendButtons(
        schemas.map((s, index) => ({
            label: s,
            action: () => {

                appendMessage(s, "user-message");

                // Backend always needs English schema
                selectedSchema = SCHEMES.English[index];

                appendMessage(
                    selectedLanguage === "Hindi"
                        ? "कृपया अपनी समस्या बताएं।"
                        : selectedLanguage === "Bengali"
                        ? "অনুগ্রহ করে আপনার সমস্যা লিখুন।"
                        : selectedLanguage === "Santali"
                        ? "Apna samasya likhiye."
                        : "Please describe your issue.",
                    "bot-message"
                );

                currentStep = "chat";
            }
        })),
        "schema"
    );
}


/* ================= SCHEME SUB OPTIONS ================= */

const SCHEME_OPTIONS = {

    English: [
        "Eligibility & Conditions",
        "Benefits",
        "How to Apply",
        "Contact Details",
        "Registration"
    ],

    Hindi: [
        "पात्रता एवं शर्तें",
        "लाभ",
        "आवेदन कैसे करें",
        "संपर्क विवरण",
        "पंजीकरण"
    ],

    Bengali: [
        "যোগ্যতা ও শর্তাবলী",
        "সুবিধাসমূহ",
        "কিভাবে আবেদন করবেন",
        "যোগাযোগের বিবরণ",
        "নিবন্ধন"
    ],

    Santali: [
        "Joggotā o Shart",
        "Labh",
        "Kena apply karbo",
        "Contact Biboron",
        "Registration"
    ]
};

function showSchemeOptions() {

    appendMessage(
        selectedLanguage === "Hindi"
            ? "कृपया नीचे दिए गए विकल्पों में से चुनें:"
            : selectedLanguage === "Bengali"
            ? "নিচের বিকল্পগুলির মধ্যে একটি নির্বাচন করুন:"
            : selectedLanguage === "Santali"
            ? "Niche diya option me se ek chayan kare:"
            : "Please choose one of the following options:",
        "bot-message"
    );

    const options = SCHEME_OPTIONS[selectedLanguage];

    appendButtons(
        options.map((opt, index) => ({
            label: opt,
            action: () => {

                appendMessage(opt, "user-message");

                // 🔥 Send English version to backend always
                const englishOption = SCHEME_OPTIONS.English[index];

                sendSchemeQuery(englishOption);
            }
        })),
        "schema"
    );
}
/* ================= SEND SCHEME QUERY TO BACKEND ================= */

function sendSchemeQuery(option) {

    showThinking();   // 🔥 THIS WILL SHOW 🤖 Typing...

    fetch(API_BASE + "/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: option,
            schema: selectedSchema
        })
    })
    .then(res => res.json())
    .then(data => {

        removeThinking();

        if (data.reply) {
            appendMessage(data.reply, "bot-message");
        } else {
            appendMessage("No response received.", "bot-message");
        }

    })
    .catch(error => {

        removeThinking();
        console.error("Scheme fetch error:", error);
        appendMessage("Server error ❌", "bot-message");

    });
}




/* ================= GENERAL OPTIONS ================= */

function showGeneralOptions() {

    appendButtons([
        { label: "Eligibility & Conditions", action: () => appendMessage("Please ask your question.", "bot-message") },
        { label: "Benefits", action: () => appendMessage("Please ask your question.", "bot-message") },
        { label: "How to Apply", action: () => appendMessage("Please ask your question.", "bot-message") },
        { label: "Contact Details", action: () => appendMessage("Please ask your question.", "bot-message") }
    ]);
}

/* ================= THINKING ================= */

let thinkingDiv = null;

function showThinking() {
    thinkingDiv = document.createElement("div");
    thinkingDiv.className = "bot-message";
    thinkingDiv.innerHTML = "🤖 Typing...";
    document.getElementById("chat-body").appendChild(thinkingDiv);
}

function removeThinking() {
    if (thinkingDiv) thinkingDiv.remove();
}


/* ================= CHAT CONTROL ================= */

function openChat() {
    document.getElementById("chat-widget").style.display = "flex";
    document.getElementById("chat-bubble").style.display = "none";
}

function closeChat() {
    document.getElementById("chat-widget").style.display = "none";
    document.getElementById("chat-bubble").style.display = "flex";
}

function toggleMaximize() {
    document.getElementById("chat-widget").classList.toggle("maximized");
}

/* ================= STT (Speech to Text) ================= */

let recognition = null;

function startRecording() {

    const micButton = document.getElementById("mic-btn");

    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Microphone not supported. Please use Google Chrome.");
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.lang =
        selectedLanguage === "Hindi" ? "hi-IN" :
        selectedLanguage === "Bengali" ? "bn-IN" :
        "en-US";

    micButton.classList.add("recording");
    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("user-input").value = transcript;
        micButton.classList.remove("recording");
        sendMessage();
    };

    recognition.onerror = function(event) {
        console.error("Mic Error:", event.error);
        micButton.classList.remove("recording");
    };

    recognition.onend = function() {
        micButton.classList.remove("recording");
    };
}



