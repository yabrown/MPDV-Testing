import os
import requests
import datetime
import time
import random
import string
import subprocess
from abc import ABC, abstractmethod
import json
from utils.node import Node

dir_path = os.path.dirname(os.path.realpath(__file__))

# Factory function to initialize the appropriate subclass
class CertificateRequestFactory:
    @staticmethod
    def create(ca_name, node_a: Node, node_b: Node):
        ca_name = ca_name.lower()
        if ca_name == "ggf":
            return GGFCertReq(node_a, node_b)
        elif ca_name == "ggp":
            return GGPCertReq(node_a, node_b)
        elif ca_name == "om":
            return OMCertReq(node_a, node_b)
        elif ca_name == "cf":
            return CFCertReq(node_a, node_b)
        elif ca_name=="le":
            return LECertREq(node_a, node_b)
        else:
            raise ValueError(f"Unknown certificate authority: {ca_name}")

class CertReq(ABC):
    def __init__(self, node_a: Node, node_b: Node):
        self.node_a = node_a
        self.node_b = node_b

    @abstractmethod
    def get_request(self, token):
        pass

    def get_results(self, token):
        try: 
            response = requests.get(f"http://{self.node_a.ip}/getips?token={token}")
            node_a_ips = response.json()['ip_addresses']
        except Exception as e:
            raise(f"Error making request to {self.node_a.name} ({self.node_a.ip}): {e}")
        try: 
            response = requests.get(f"http://{self.node_b.ip}/getips?token={token}")
            node_b_ips = response.json()['ip_addresses']
        except Exception as e:
            raise(f"Error making request to {self.node_b.name} ({self.node_b.ip}): {e}")
        return node_a_ips, node_b_ips

    # Get a successful request and returns the corresponding 
    def send_request(self):
        retries = 5
        for attempt in range(retries):
            response, token = self._single_request()
            if response.status_code == 200:
                return token
            elif attempt < retries - 1:
                print(f"Attempt {attempt + 1} failed with status code {response.status_code}. Waiting 10 seconds and retrying...")
                time.sleep(10)
            else:
                # log error
                with open(f"{dir_path}/results/errors.log", 'a') as file:
                    file.write(f"{self.node_a.name},{self.node_b.name}:\tHTTP Error: Failed after {retries} attempts with final status code {response.status_code}\n")
    
    def _single_request(self):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=21)) # ClourFlare requires a 21 character token, or it'll respond with a 400-- "Not enough entropy in token"
        cert_req =self.get_request(token)
        response = requests.post(**cert_req)
        with open(f"{dir_path}/results/http.log", 'a') as file:
            now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'
            file.write(f"\t{now} {cert_req}\n")
            print(f"\t{now} {cert_req}")
            file.write(f"\t{now} {response.text}\n")
            print(f"\t{now} {response.text}\n")
        return response, token
        


class OMCertReq(CertReq):
    def get_request(self, token):
        return {
            "url": "https://anor3x6mtj.execute-api.us-east-2.amazonaws.com/v1/mpic",
            "headers": {
            "Content-Type": "application/json",
            "x-api-key": os.environ['MPIC_API_KEY']
            },
            "json": {
                "orchestration_parameters": {
                    "perspective_count": 13,
                    "max_attempts": 1
                },
                "check_type": "dcv",
                "domain_or_ip_target": "123233.arins.pretend-crypto-wallet.com",
                "dcv_check_parameters": {
                    "validation_method": "http-generic",
                    "validation_details": {
                        "http_token_path": f"validate?token={token}",
                        "challenge_value": "test"
                    }
            }
            }
        }

class GGFCertReq(CertReq):
    def get_request(self, token):
        return {
            "url": "http://35.211.239.179:5000/run-all",
            "headers": {
                "Content-Type": "application/json"
            },
            "json": {
                "domain": "123123123.arins.pretend-crypto-wallet.com",
                "token": token,
                "node_a": self.node_a.name,
                "node_b": self.node_b.name,
            }
        }

class GGPCertReq(CertReq):
    def get_request(self, token):
        return {
            "url": "http://34.75.246.52:5000/run-all",
            "headers": {
                "Content-Type": "application/json"
            },
            "json": {
                "domain": "123123123.arins.pretend-crypto-wallet.com",
                "token": token,
                "node_a": self.node_a.name,
                "node_b": self.node_b.name,
            }
        }

class CFCertReq(CertReq):
    def get_request(self, token):

        return {
            "url": "https://dcvcheck.cloudflare.com/mpdcv/v1",
            "headers": {
                "Content-Type": "application/json"
            },
            "json": {
                "method": "acme/http-01",
                "kaHash": "TfPD9o_Mg7J-nULJBDGnJJnxeHXIGlmbVmyYiblpZwM=",
                "token": token,
                "domain": "37395983.arins.pretend-crypto-wallet.com",
                "accessToken": "YTrWJscsDU2BJNF_AUaXjg=="
            }
        }
    
class LECertREq(CertReq):
    def get_request():
        return
    def send_request(self):
        certbot_tools = "~/certbot_tools"
        subprocess.run([
            "certbot",
            "certonly",
            "--manual",
            "--manual-auth-hook", f"{certbot_tools}/authenticator.sh",
            "--manual-cleanup-hook", f"{certbot_tools}/cleanup.sh",
            "--dry-run",
            "-d", "sajghfgfhsdfasdf.arins.pretend-crypto-wallet.com"
        ])
        with open(os.path.expanduser(f"{certbot_tools}/token"), "r") as file:
            return file.read().strip()
