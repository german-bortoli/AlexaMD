from __future__ import print_function
import json
import urllib2
from random import choice as rc

POST_URL = "http://52.88.102.80/harambe/diagnosis"

GREETS_1 = [
    "Awwww, what's wrong?",
    "Oh dear, is everything alright?",
    "Oh no, are you okay?"
]
GREETS_2 = [
    "I'll try my best to help out.",
    "I'll do my best to help you.",
    "I'll see what I can do."
]
GREETS_3 = [
    "Could you tell me your symptoms, one at a time please?",
    "I need to know your symptoms, one at a time please."
]

'''
START_PROMPTS = [
    "Okay. Please tell me your symptoms, one at a time.",
    "So, I need to know your symptoms, one at a time please."
]
'''

APOLOGY_1 = [
    "I'm so sorry!",
    "Sorry about that.",
    "Whoops!",
    "My bad."
]
APOLOGY_2 = [
    "My voice recognition can be a bit dodgy at times.",
    "It would be nice to have a real pair of ears.",
    "Could you try speaking a bit more clearly?",
    "I wish Amazon would hire Joshua Li to improve my natural language processing."
]
APOLOGY_3 = [
    "Any more symptoms?",
    "Any other symptoms I should know about?"
]

# --------------- Functions that control the skill's behavior ----------------


def get_welcome_response():
    sesh_attribs = {'symptoms': [], 'age': '10', 'sex': 'male', 'name': 'Josh'}
    # TODO get age name and sex, need to make a new action
    speech_output = ' '.join([rc(GREETS_1), rc(GREETS_2), rc(GREETS_3)])
    reprompt_text = "Could you tell me your symptoms, one at a time please?"
    return build_response(sesh_attribs, build_speechlet_response("Welcome", speech_output, reprompt_text, False))


def add_symptom(symptom, session):
    s_list = session['attributes']['symptoms']
    s_list.append(symptom)
    return {
        'symptoms': s_list,
        'age': session['attributes']['age'],
        'sex': session['attributes']['sex'],
        'name': session['attributes']['name']
    }


def pop_symptom(session):
    s_list = session['attributes']['symptoms']
    return {
        'symptoms': s_list[:-1],
        'age': session['attributes']['age'],
        'sex': session['attributes']['sex'],
        'name': session['attributes']['name']
    }


def get_diagnosis(symptom_list, age, sex):
    data = json.dumps({
        'age': age,
        'sex': sex,
        'symptoms': symptom_list
    })
    req = urllib2.Request(POST_URL, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    d = json.load(f)
    f.close()
    return d['diagnosis']


'''
def request_user_info(intent, session):
    card_title = intent['name']
    sesh_attribs = session['attributes']
    speech_output = "I just need to know a bit about you. What's your name, age, and are you male or female?"
    reprompt_text = speech_output
    return build_response(sesh_attribs, build_speechlet_response(card_title, speech_output, reprompt_text, False))


def get_user_info(intent, session):
    card_title = intent['name']
    sesh_attribs = session['attributes']

    if 'Name' in intent['slots'] and 'Age' in intent['slots'] and 'Sex' in intent['slots']:
        name = intent['slots']['Name']['value']
        age = intent['slots']['Age']['value']
        sex = intent['slots']['Sex']['value']
        update_user(session, name, age, sex)
        speech_output = rc(START_PROMPTS).format(sesh_attribs['name'])
        reprompt_text = speech_output

    else:
        speech_output = "Sorry, I'm not sure what you mean. Maybe try putting it in a different way?"
        reprompt_text = speech_output

    return build_response(sesh_attribs, build_speechlet_response(card_title, speech_output, reprompt_text, False))
'''


def set_symptoms_in_session(intent, session):
    card_title = intent['name']
    sesh_attribs = session['attributes']

    if 'Symptom' in intent['slots']:
        symptom = intent['slots']['Symptom']['value']

        if symptom in ["that's it", "no", "nope", "nothing else", "nah"]:
            diagnosis_string = get_diagnosis(sesh_attribs['symptoms'], sesh_attribs['age'], sesh_attribs['sex'])
            return build_response(sesh_attribs, build_speechlet_response("Session Ended", diagnosis_string, None, True))

            # TODO do more things after here after merely telling diagnosis

        elif symptom in ['right']:
            speech_output = "Your symptoms are " + ', '.join(sesh_attribs['symptoms']) + ". Anything else?"
            reprompt_text = "Any other symptoms I should know about?"
            return build_response(sesh_attribs, build_speechlet_response(card_title, speech_output, reprompt_text, False))

        elif symptom in ['wrong']:
            sesh_attribs = pop_symptom(session)
            speech_output = ' '.join([rc(APOLOGY_1), rc(APOLOGY_2), rc(APOLOGY_3)])
            reprompt_text = "Any other symptoms I should know about?"
            return build_response(sesh_attribs, build_speechlet_response(card_title, speech_output, reprompt_text, False))

        else:
            sesh_attribs = add_symptom(symptom, session)
            speech_output = "Is " + symptom + " right or wrong?"
            reprompt_text = speech_output
            return build_response(sesh_attribs, build_speechlet_response(card_title, speech_output, reprompt_text, False))

    else:
        speech_output = "I'm not sure what you mean by " + symptom + "."
        reprompt_text = speech_output

    return build_response(sesh_attribs, build_speechlet_response(card_title, speech_output, reprompt_text, False))


def handle_session_end_request():
    return build_response({}, build_speechlet_response("Session Ended", "Goodbye. I hope you get well soon.", None, True))

# --------------- Intent Events ------------------


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "MySymptomsAreIntent":
        return set_symptoms_in_session(intent, session)
    # elif intent_name == "GetUserInfoIntent":
    #    return get_user_info(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


# --------------- Other Events ------------------


def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return get_welcome_response()


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(sesh_attribs, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': sesh_attribs,
        'response': speechlet_response
    }


# --------------- Main handler ------------------


def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])