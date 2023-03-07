import re
import csv
import operator

errors = {} #dictionary for errors
per_users = {}  #dict for users
dir = ''  #the directory of the log's file
log_name = ''  #name of the log's file., e.g, LOGS.txt

'''logs look like: 
Jan 31 17:29:11 ubuntu.local ticky: ERROR Connection to DB failed (oren)
Jan 31 17:51:52 ubuntu.local ticky: INFO Closed ticket [#8604] (mcintosh)
Jan 31 18:09:17 ubuntu.local ticky: ERROR The ticket was modified while updating (noel)
Jan 31 18:43:01 ubuntu.local ticky: ERROR Ticket doesn't exist (nonummy)
Jan 31 19:00:23 ubuntu.local ticky: ERROR Timeout while retrieving information (blossom)'''

with open(dir+log_name) as logs:
        error_pattern = r"ticky: ERROR ([\w ]*)" #pattern for errors (with the log message) in a log
        info_pattern = r"INFO"  #pattern for info in a log
        user_pattern = r"\(([\w\.?]*)\)"    #pattern for a user
        #iterating through the logs
        for log in logs:
            user = re.search(user_pattern, log).group(1)  # capturing username in the given log
            if user not in per_users.keys():    #if username is not in a dict then adding them and assigning with an empty
                # 2 element list, where the 0 element stands for info-instances, 1st element - for error instances
                per_users[user] = [0, 0]

            if re.search(info_pattern, log):    #if the log contains INFO, then appending 1 to the user in a dict,
                # namely, to the 0 position of the list
                if user not in per_users:
                    per_users[user] = []
                    per_users[user][0] = 1
                else:
                    per_users[user][0] += 1

            if re.search(error_pattern, log):   #if the log contains ERROR, then appending 1 to the user in a dict,
                # namely, to the 1 position of the list
                if user not in per_users:
                    per_users[user] = []
                    per_users[user][1] = 1
                else:
                    per_users[user][1] += 1

                #appending to the errors' dict
                error = re.search(error_pattern, log).group()   #capturing the ERROR message from the log
                if error not in errors: # if the ERROR message is not in the dict, then append 1
                    errors[error] = 1
                else:
                    errors[error] += 1

per_users = sorted(per_users.items())   #sorting users' dict alphabetically
errors = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)   # sorting by the number of errors, DESC order
errors.insert(0, ("ERROR", "COUNT"))    #inserting the headers to the errors list

#creating csv file with error messages 'error_message.csv'
with open(dir + '/error_message.csv', 'w') as output_error:
    writer = csv.writer(output_error)
    writer.writerows(errors)
    output_error.close()

#creating scv file with users' statistics 'user_statistics.csv'
with open(dir + '/user_statistics.csv', 'w', newline='') as output_users:
    fieldnames = ["Username", "INFO", "ERROR"]  #creating headers
    writer = csv.DictWriter(output_users, fieldnames=fieldnames)
    writer.writeheader()
    # for each key and value from per_users list appending to the scv file into the corresponding header,
    # remembering that it has a form (user, [0, 0]), e.g., ('ahmed.miller', [2, 4]), where 'ahmed.miller'
    # is username; [2, 4] - 2 instances of INFO and 4 instances of ERROR from this user
    for key, value in per_users:
        writer.writerow({"Username": str(key), "INFO": str(value[0]), "ERROR": str(value[1])})
