# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2022-2023 Dyne.org foundation <foundation@dyne.org>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Module for GC1DPP (Global Circularity 1 Digital Product Passport) integration
"""

import json
import hashlib
import requests
import base64
from typing import Dict, Any, Optional, Tuple
from zenroom import zenroom


def calculate_file_checksum(file_path: str) -> str:
    """
    Calculate SHA-256 checksum of a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        Hex string of the checksum
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def sign_message(message: str, eddsa_private_key: str, encode_base64: bool = False) -> Tuple[str, str]:
    """
    Sign a message using EdDSA private key with Zenroom (matching GUI/DPP service format)
    
    There are TWO modes in the GUI:
    
    1. File uploads (encode_base64=False):
       - SignMessage(checksum) passes raw hex checksum directly
       - Used for: upload_file_on_dpp
       
    2. DPP/signedPost (encode_base64=True):
       - signDidRequest(json) base64-encodes the JSON first
       - Used for: submit_dpp (POST /dpp)
       
    Args:
        message: Message to sign (raw string for mode 1, JSON string for mode 2)
        eddsa_private_key: EdDSA private key
        encode_base64: If True, base64-encode the message before signing (for DPP submission)
        
    Returns:
        Tuple of (signature as base64, hash as hex)
    """
    # This sign script matches verify_graphql.zen used by the DPP server
    sign_script = """
    Scenario eddsa: sign a message
    Given I have a 'base64' named 'gql'
    Given I have a 'keyring'
    When I remove spaces in 'gql'
    and I compact ascii strings in 'gql'
    When I create the eddsa signature of 'gql'
    And I create the hash of 'gql'
    Then print 'eddsa signature' as 'base64'
    Then print 'hash' as 'hex'
    """
    
    # Handle the two different signing modes from the GUI
    if encode_base64:
        # Mode 2: signDidRequest - base64 encode the JSON body first
        # GUI: Buffer.from(json, "utf8").toString("base64")
        message_for_sign = base64.b64encode(message.encode('utf-8')).decode('utf-8')
    else:
        # Mode 1: SignMessage for file uploads - pass raw checksum
        message_for_sign = message
    
    data = json.dumps({"gql": message_for_sign})
    keys = json.dumps({"keyring": {"eddsa": eddsa_private_key}})
    
    result = zenroom.zencode_exec(sign_script, keys=keys, data=data)
    
    # Debug output if Zenroom fails
    if not result.output:
        print(f"Zenroom returned empty output!")
        print(f"Zenroom logs: {result.logs[:1000] if result.logs else 'none'}")
        print(f"Message length: {len(message)}")
        raise Exception(f"Zenroom sign failed: {result.logs[:500] if result.logs else 'no logs'}")
    
    result_json = json.loads(result.output)
    
    return result_json['eddsa_signature'], result_json['hash']
    
    return result_json['eddsa_signature'], result_json['hash']


def upload_file_on_dpp(file_path: str, eddsa_public_key: str, eddsa_private_key: str, dpp_url: str) -> Dict[str, Any]:
    """
    Upload a file to the DPP service
    
    Args:
        file_path: Path to the file to upload
        eddsa_public_key: EdDSA public key for authentication
        eddsa_private_key: EdDSA private key for signing
        dpp_url: Base URL of the DPP service
        
    Returns:
        Dictionary with attachment response containing id, fileName, contentType, url, size, checksum, uploadedAt
    """
    # Calculate checksum
    checksum = calculate_file_checksum(file_path)
    print(f"File checksum: {checksum}")
    
    # Sign the checksum
    signature, hash_val = sign_message(checksum, eddsa_private_key)
    
    # Prepare the file upload
    with open(file_path, 'rb') as f:
        files = {'file': f}
        headers = {
            'did-pk': eddsa_public_key,
            'did-sign': signature
        }
        
        response = requests.post(
            f"{dpp_url}/upload",
            headers=headers,
            files=files
        )
    
    if not response.ok:
        try:
            err = response.json()
            error_msg = err.get('error', response.text)
        except:
            error_msg = response.text
        raise Exception(f"Upload failed: {error_msg}")
    
    return response.json()


def process_dpp_values(obj: Any, eddsa_public_key: str, eddsa_private_key: str, dpp_url: str) -> Any:
    """
    Process DPP values recursively, uploading files and replacing them with attachment responses
    
    Args:
        obj: Object to process (can be dict, list, str, or file path)
        eddsa_public_key: EdDSA public key for authentication
        eddsa_private_key: EdDSA private key for signing
        dpp_url: Base URL of the DPP service
        
    Returns:
        Processed object with files replaced by attachment responses
    """
    if obj is None:
        return obj
    
    # Check if it's already an attachment response (already uploaded image)
    # These have 'id' and 'url' keys from the DPP service
    if isinstance(obj, dict) and obj.get('id') and obj.get('url'):
        # Already an attachment response, return as-is
        return obj
    
    # Check if it's a file path (string ending with common file extensions)
    # Only try to upload if it looks like an actual path (contains / or \) or exists on disk
    if isinstance(obj, str) and any(obj.endswith(ext) for ext in ['.pdf', '.png', '.jpg', '.jpeg', '.gif', '.txt', '.doc', '.docx']):
        # Skip if it's just a filename without path (likely from an existing attachment response)
        import os
        if '/' not in obj and '\\' not in obj and not os.path.exists(obj):
            # It's just a filename, not an actual file path - skip upload
            return obj
        # Try to upload as a file
        try:
            return upload_file_on_dpp(obj, eddsa_public_key, eddsa_private_key, dpp_url)
        except Exception as e:
            print(f"Warning: Could not upload file {obj}: {e}")
            return obj
    
    if isinstance(obj, list):
        return [process_dpp_values(item, eddsa_public_key, eddsa_private_key, dpp_url) for item in obj]
    
    if isinstance(obj, dict):
        processed_obj = {}
        for key, value in obj.items():
            processed_obj[key] = process_dpp_values(value, eddsa_public_key, eddsa_private_key, dpp_url)
        return processed_obj
    
    return obj


def submit_dpp(dpp_data: Dict[str, Any], eddsa_public_key: str, eddsa_private_key: str, dpp_url: str) -> str:
    """
    Submit a DPP to the DPP service.
    
    Matches GUI signedPost(DPP_URL/dpp, processedDpp, did=true) flow:
    1. Process DPP values (upload files, replace with AttachmentResponse)
    2. Serialize processed DPP to JSON string
    3. Sign the JSON string using signDidRequest pattern
    4. POST with did-pk and did-sign headers
    
    Args:
        dpp_data: DPP data to submit (will be processed for file uploads)
        eddsa_public_key: EdDSA public key for authentication
        eddsa_private_key: EdDSA private key for signing
        dpp_url: Base URL of the DPP service
        
    Returns:
        ULID of the inserted DPP
    """
    # Process the DPP data to upload any files
    processed_dpp = process_dpp_values(dpp_data, eddsa_public_key, eddsa_private_key, dpp_url)
    
    # Serialize to JSON string (this is the body that will be sent)
    # GUI uses JSON.stringify(request) for both signing and body
    body_json = json.dumps(processed_dpp)
    
    # Sign the JSON body - use encode_base64=True to match GUI signDidRequest
    # which does: Buffer.from(json, "utf8").toString("base64")
    signature, hash_val = sign_message(body_json, eddsa_private_key, encode_base64=True)
    
    # Submit the DPP with DID headers
    headers = {
        'did-pk': eddsa_public_key,
        'did-sign': signature,
        'Content-Type': 'application/json'
    }
    
    print(f"Submitting DPP to {dpp_url}/dpp")
    print(f"Public key: {eddsa_public_key[:20]}...")
    print(f"Signature: {signature[:40]}...")
    
    # Send the exact same JSON string that was signed
    response = requests.post(
        f"{dpp_url}/dpp",
        headers=headers,
        data=body_json  # Use data= with the exact signed string, not json=
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text[:500] if response.text else '(empty)'}")
    
    if not response.ok:
        error_msg = f"Failed to submit DPP: {response.status_code} {response.text}"
        print(error_msg)
        print(f"Headers sent: {headers}")
        raise Exception(error_msg)
    
    result = response.json()
    dpp_ulid = result.get('insertedID')
    print(f"DPP submitted with ULID: {dpp_ulid}")
    
    return dpp_ulid


def create_sample_bike_dpp() -> Dict[str, Any]:
    """
    Create a sample DPP for the fancy collaborative bike
    
    Returns:
        Sample DPP data structure
    """
    return {
        "productOverview": {
            "brandName": {"type": "string", "value": "Fancy Collaborative Bikes"},
            "productName": {"type": "string", "value": "Fancy Collaborative Bike"},
            "productDescription": {"type": "string", "value": "A collaborative bike made with funky design, aluminum frame, and magic mirror"},
            "countryOfOrigin": {"type": "string", "value": "Netherlands"},
            "color": {"type": "string", "value": "Custom"},
            "netWeight": {"type": "number", "value": 15, "units": "kg"},
            "modelName": {"type": "string", "value": "FCB-2025"}
        },
        "reparability": {
            "availabilityOfSpareParts": {"type": "string", "value": "Available through manufacturer network"}
        },
        "environmentalImpact": {
            "co2eEmissionsPerUnit": {"type": "number", "value": 45, "units": "kg"},
            "minimumContentOfMaterialWithSustainabilityCertification": {"type": "number", "value": 60, "units": "%"}
        },
        "components": [
            {
                "componentDescription": {"type": "string", "value": "Aluminum Bike Frame"},
                "componentGTIN": {"type": "string", "value": "aluminum-frame-001"}
            },
            {
                "componentDescription": {"type": "string", "value": "Magic Bike Mirror"},
                "componentGTIN": {"type": "string", "value": "magic-mirror-001"}
            }
        ],
        "economicOperator": {
            "companyName": {"type": "string", "value": "Farback"},
            "addressLine1": {"type": "string", "value": "Prins Hendrikkade 82 A"},
            "addressLine2": {"type": "string", "value": "1012 AE, Amsterdam, Netherlands"}
        },
        "recyclability": {
            "materialComposition": {"type": "string", "value": "Aluminum: 80%, Glass: 5%, Other materials: 15%"}
        }
    }
