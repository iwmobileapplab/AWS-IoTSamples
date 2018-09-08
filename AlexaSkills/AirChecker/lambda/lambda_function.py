"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Alexa Air Checker - " + title,  # "SessionSpeechlet - " + title,
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


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the atomosphere analyzer."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What's going on?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "TemperatureIntent":
        return get_temperature(intent, session)
    elif intent_name == "HumidityIntent":
        return get_humidity(intent, session)
    elif intent_name == "PressureIntent":
        return get_pressure(intent, session)
    elif intent_name == "AllIntent":
        return get_all(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


import boto3
import json
import decimal
import time
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


# --------------- Helpers to convert a DynamoDB item to JSON -------------

class DecimalEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def get_temperature(intent, session):
    """ Gets temperature data from DynamoDB
    """

    res = query()
    session_attributes = {}

    if len(res['Items']) is 0:
        return build_response(session_attributes, build_no_data_response())

    return_response = max(res["Items"], key=(lambda x: x["Timestamp"]))
    latest_record = json.dumps(return_response, default=decimal_default)

    json_obj = json.loads(latest_record)
    timestamp = json_obj['Timestamp']
    temperature = json_obj['payload']['Temperature']
    temperature = str(int(temperature))

    speech_output = 'The temperature is ' + temperature + ' degrees celsius'
    # get formatted date time text from time stamp: 2018-09-03 15:12:10
    date_text = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(int(timestamp) / 1000))

    return build_response(session_attributes, build_speech_response(date_text, speech_output))


def get_humidity(intent, session):
    """ Gets humidity data from DynamoDB
    """

    res = query()
    session_attributes = {}

    if len(res['Items']) is 0:
        return build_response(session_attributes, build_no_data_response())

    return_response = max(res["Items"], key=(lambda x: x["Timestamp"]))
    latest_record = json.dumps(return_response, default=decimal_default)

    json_obj = json.loads(latest_record)
    timestamp = json_obj['Timestamp']
    humidity = json_obj['payload']['Humidity']
    humidity = str(int(humidity))

    speech_output = 'The humidity is ' + humidity + ' percent.'
    date_text = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(int(timestamp) / 1000))

    return build_response(session_attributes, build_speech_response(date_text, speech_output))


def get_pressure(intent, session):
    """ Gets pressure data from DynamoDB
    """

    res = query()
    session_attributes = {}

    if len(res['Items']) is 0:
        return build_response(session_attributes, build_no_data_response())

    return_response = max(res["Items"], key=(lambda x: x["Timestamp"]))
    latest_record = json.dumps(return_response, default=decimal_default)

    json_obj = json.loads(latest_record)
    timestamp = json_obj['Timestamp']
    pressure = json_obj['payload']['Pressure']
    pressure = str(int(pressure))

    speech_output = 'The pressure is ' + pressure + ' hPs.'
    date_text = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(int(timestamp) / 1000))

    return build_response(session_attributes, build_speech_response(date_text, speech_output))


def get_all(intent, session):
    """ Get all kinds of data from DynamoDB
    """

    res = query()
    session_attributes = {}

    if len(res['Items']) is 0:
        return build_response(session_attributes, build_no_data_response())

    return_response = max(res["Items"], key=(lambda x: x["Timestamp"]))
    latest_record = json.dumps(return_response, default=decimal_default)

    json_obj = json.loads(latest_record)
    timestamp = json_obj['Timestamp']
    temperature = json_obj['payload']['Temperature']
    temperature = str(int(temperature))
    pressure = json_obj['payload']['Pressure']
    pressure = str(int(pressure))
    humidity = json_obj['payload']['Humidity']
    humidity = str(int(humidity))

    speech_output = 'The temperature is ' + temperature + ' degrees celsius and humidity is ' + \
        humidity + ' percent. Finally, pressure is ' + pressure + ' hectopascal.'
    date_text = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(int(timestamp) / 1000))

    return build_response(session_attributes, build_speech_response(date_text, speech_output))


def query():

    now = time.time()
    start = now - (24 * 60 * 60)  # 24 hours
    now = str(int(now * 1000))
    start = str(int(start * 1000))

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('SensorData')
    return table.query(
        KeyConditionExpression=Key('DeviceId').eq("esp32_E67D94") & Key('Timestamp').between(start, now),
        ScanIndexForward=False,
        Limit=1
    )


def build_speech_response(date_text, speech_output):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': speech_output
        },
        'card': {
            'type': 'Simple',
            'title': 'Alexa Air Checker',
            'content': date_text + '\n' + speech_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': ''
            }
        },
        'shouldEndSession': True
    }


def build_no_data_response():
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'There is no data available for the last 24 hours'
        },
        'card': {
            'type': 'Simple',
            'title': 'Alexa Air Checker',
            'content': 'There is no data available for the last 24 hours'
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': ''
            }
        },
        'shouldEndSession': True
    }
