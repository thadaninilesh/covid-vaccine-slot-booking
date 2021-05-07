# covid-vaccine-slot-booking

To search slots by pincodes, checkout search_by_pincode branch
To search slots by districts, checkout search_by_district branch

One can simply use the .exe file and provide the necessary information

Prequisites - 
1. python3
2. pip


Follow these steps when running the script - 
1. Goto the root directory and run pip install -r requirements.txt. This will install all the needed dependencies
2. Run the script using the following command - 
   py src/covid-vaccine-slot-booking.py
   
Execution steps - 
1. Provide the mobile number and wait for OTP (OTP needs to be entered every 15 minutes)
2. Select the beneficiaries using the idx (comma separated. Example - 1,2,3)
3. If 3 beneficiaries are selected, enter 3 when asked 'Filter out centers with availability less than:'. If 2 are selected, enter 2. And so on
4. If search by pincode, enter comma separated pincodes (Eg - 400001,400002)
5. If search by district, 1st select state, then district from the list shown

Please note, CoWIN platform has been continuously changing the way their APIs work. So this might not work after a while. Feel free to raise a bug and I'll try to fix it. 
