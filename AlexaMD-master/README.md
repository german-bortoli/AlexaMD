Inspiration
Around the world, thousands of people are reluctant to go to doctors due to the rising cost of health care. A single visit, for those with lower insurance can range from $80-200, depending on the severity of the condition. Seeing this as a huge problem, we ventured on the mission to bring affordable medical diagnoses to the homes of real people.

What it does
Rather than completely replacing the physician, AlexaMD serves to diagnose more common and minuscule conditions, may it be the common cold or the flu. However, she is also trained to diagnose larger, and more series conditions. AlexaMD works by engaging in real conversations with the patient. She is activated when the patient tells her that he/she isn't feeling well, and after a short conversation, she can report on the condition, or send the patient to a doctor for further diagnosis. We do realize that computer-based diagnoses are not completely accurate, so Dr. Alexa will always recommend the doctor.

How we built it
AlexaMD consists of 3 main systems: the Amazon Echo, AWS Lambda, AlexaAPI. The Amazon Echo is the central point of communication between Dr. Alexa and the patient. Through the Echo, we are able to not only get patient symptom input, but also return real human phrases to the patient to provide genuine interactions. One step behind the Echo, we have our AWS Lambda instance. We used Lambda to actually outline the conversation between the Echo and the patient. Essentially, we had expected phrases on Lambda used to gain user feedback, and based on that feedback we made API calls to retrieve the correct diagnoses. Lastly, we built an API for Alexa on AWS EC2 that was able to take in symptoms, and generate the most likely problems. We used a 3rd party API to grab potential illnesses and then ranked them for the patient. In the API, we also implemented our own natural language processing algorithm so that we could have more natural conversations with the patient.

Challenges we ran into
The main challenges we ran into were with Amazon Lambda and our API creation. It was our first time working with the Echo, and we were not too familiar with the technology. The biggest challenge with Lambda that we had was making sure that the exact symptoms we wanted were parsed, and the interaction wouldn't be awkward. Going off of that, on the API side, the biggest challenge we ran into was the natural language processing. As many medical terms are long and difficult for the common person, we wanted to make sure that we could not only have an effective system, but also ensure that the conversation was smooth.

Accomplishments that we're proud of
Overall, we are most proud of building something that has a real potential to help people. With our 24 hours of work, we were able to create a device capable of providing a service to people at a price point that's very affordable. In addition to the impact of our work, we are equally proud of the technology feats. We were able to build a full stack system, where we not only implemented natural language process from scratch, but we also allowed for fast, and seamless user experience.

What we learned
As with any hackathon, this one was also filled with learning. For all of us, it was the first time really working with Lambda, and for many members of the team, AWS. Additionally, we learned about the difficulty and cool algorithmic nature of NLP, and will definitely do more with it.

What's next for AlexaMD
AlexaMD is just the beginning of a medical revolution. We strive to bring major feats to healthcare that can truly help real people. We believe that by using the advanced devices we have today (like Fitbits, Smart Watches, etc), we can combine them with the huge database of information, to bring the best and most innovative solutions for tomorrow. With AlexaMD, we were able to use one of these amazing technology devices, so in the future, we strive to do so much more.
