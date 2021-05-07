import copy
from collections import Counter
import requests, sys, argparse, os
from utils import generate_token_OTP, get_beneficiaries, check_and_book, get_districts, get_min_age, beep, \
    BENEFICIARIES_URL, WARNING_BEEP_DURATION
import traceback

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='Pass token directly')
    args = parser.parse_args()

    mobile = None
    try:
        base_request_header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
        
        if args.token:
            token = args.token
        else:
            mobile = input("Enter the registered mobile number: ")
            token = generate_token_OTP(mobile, base_request_header)

        request_header = copy.deepcopy(base_request_header)
        request_header["Authorization"] = f"Bearer {token}"
        
        # Get Beneficiaries
        print("Fetching registered beneficiaries.. ")
        beneficiary_dtls = get_beneficiaries(request_header)

        if len(beneficiary_dtls) == 0:
            print("There should be at least one beneficiary. Exiting.")
            os.system("pause")
            sys.exit(1)

        # Make sure all beneficiaries have the same type of vaccine
        vaccine_types = [beneficiary['vaccine'] for beneficiary in beneficiary_dtls]
        vaccines = Counter(vaccine_types)

        if len(vaccines.keys()) != 1:
            print(f"All beneficiaries in one attempt should have the same vaccine type. Found {len(vaccines.keys())}")
            os.system("pause")
            sys.exit(1)

        # Set filter condition
        minimum_slots = int(input('Filter out centers with availability less than: '))
        minimum_slots = minimum_slots if minimum_slots > len(beneficiary_dtls) else len(beneficiary_dtls)

        # Comma separated pincodes
        pincodes_str = input('Enter comma separated pincodes to search vaccine centers in : ')
        pincodes = pincodes_str.split(',')

        token_valid = True
        while token_valid:
            request_header["Authorization"] = f"Bearer {token}"

            # call function to check and book slots
            token_valid = check_and_book(request_header, beneficiary_dtls, minimum_slots, pincodes)

            # check if token is still valid
            beneficiaries_list = requests.get(BENEFICIARIES_URL, headers=request_header)
            if beneficiaries_list.status_code == 200:
                token_valid = True

            else:
                # if token invalid, regenerate OTP and new token
                beep(WARNING_BEEP_DURATION[0], 1000)
                print('Token is INVALID.')
                token_valid = False

                token = generate_token_OTP(mobile, request_header)
                token_valid = True

    except Exception as e:
        print(str(e))
        traceback.print_exc()
        print('Exiting Script')
        os.system("pause")


if __name__ == '__main__':
    main()
