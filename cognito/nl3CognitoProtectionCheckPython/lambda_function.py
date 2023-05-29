import json
import os
import requests
import base64
import logging
from datetime import datetime
import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getLockStatus(token, api_uri, api_path, validationData):
  responseDict = {}
  try:
    
    headers_dict = {
      "x-nl3-authorization-token": token, 
      "Content-Type": "application/json",
      "x-nl3-device-location": json.loads(validationData["additionalData"])["loc"],
      "x-forwarded-for": validationData["ip"],
      "User-Agent": validationData["device"]
    }
    
    data_dict = {
      "userIP": validationData["ip"],
      "userDevice": validationData["device"],
      "userLocation": validationData["location"],
      "integrationType": "cognito",
      "integrationData": json.loads(validationData["additionalData"])
    }
    

    response = requests.post("".join([api_uri,api_path]), headers=headers_dict, json=data_dict)

    responseDict = response.json()
  except Exception as e:
    responseDict = { "message": str(e) }

  return responseDict

def lambda_handler(event, context):
  logger.info(event);
  logger.info(context);
  if event["callerContext"]["clientId"] == os.environ["CLIENT_ID"]:
    username = event["userName"]
    claims = {
      "iss": os.environ["APP_FQDN"],
      "iat": (datetime.utcnow().timestamp() + (-1 * 60)),
      "exp": (datetime.utcnow().timestamp() + (5 * 60)),
      "aud": os.environ["API_URI"],
      "sub": username
    }
    decodedDomainToken = base64.b64decode(os.environ["SIGNING_KEY"])
    token = jwt.encode(
      payload=claims,
      key=decodedDomainToken
    )
    logger.info(event["request"]["validationData"])
    response = getLockStatus(token, os.environ["API_URI"], os.environ["API_PATH"], event["request"]["validationData"])
    logger.info(response)
    # CHANGE False to True on following line to fail closed!!
    if response.get("locked", False):
      logger.info("Locked == True If statement!")
      raise Exception(os.environ["LOCKED_MESSAGE"])

    # Return to Amazon Cognito
    return event