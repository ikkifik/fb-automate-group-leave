### FB Automate Group Leave (for lazy person)

FB Automate Group Leave (for lazy person), if you are not lazy enough just do the manual left by visiting one-by-one your group.  

This program required group list to defined inside file named 'targeted_group.txt', fill with the same group name otherwise you will fail to left the group automatically using this program.  

##### How to Install (Python)

    1. git clone  
    2. python3 -m venv fbvenv  
    3. source fbvenv/bin/activate  
    4. pip install -r requirements.txt

##### Get your targeted group

    Open targeted_group.txt file, fill it with group list you want to leave separated with line break,  
    like this:

    group_a_learning
    group_b_work
    group_c_study

##### Run Program
    
    python leave_group.py --email <your_fb_email_account> --pwd <your_fb_password_account>  

----

Also see the preview: 