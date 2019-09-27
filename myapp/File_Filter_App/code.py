import pandas as pd
from os.path import basename
from datetime import datetime, timedelta

class Airtel_AV_Dashboard:
    def __init__(self, flag):
        self.flag = flag

    def process(self, filepath, filename):
        #Since file name has path "documents/2019/09/24/Raw Data/" len=19 strip them off
        filename =  basename(filepath)
        
        daytime = datetime(2019, 9, 6)


        n_1 = daytime - timedelta(days=1)
        cur_t = n_1.strftime('%Y-%m-%d')
        new_time = n_1 -timedelta(days=8)
        new_time = new_time.strftime('%Y-%m-%d')
        n_7 = n_1 -timedelta(days=8)
        new_7 = n_7.strftime('%Y-%m-%d')
        n_30 = n_1 -timedelta(days=30)
        new_30 = n_30.strftime('%Y-%m-%d')
        n_3 = n_1-timedelta(days=3)
        new_3 = n_3.strftime('%Y-%m-%d')


        df_tmp = pd.read_csv(filepath)
        df = df_tmp[['Pattern Date','Revision','Version','Operating System','Computer Name','IP Address1','Group Name','Current User']]


        df_wtNA = df[df['Pattern Date'].str.contains("NaN")==False]   ### remove NA from pattern date
        #df_wtNA = df_wtNA.sort_values('Pattern Date', inplace=True)  ## sort values by acssending order


        df_wtS = df_wtNA[df_wtNA['Operating System'].str.contains("Server")==True] #Filter for server on operating system

        df_wtC =df_wtNA[ df_wtNA['Operating System'].str.contains('Server')==False] #Filter for client on operating system


        df_wtDUS = df_wtS.drop_duplicates('IP Address1', keep='first') ## remove duplicacy from server

        df_wtDUC = df_wtC.drop_duplicates('Computer Name', keep='first') # remove duplicacy from client

        df_2 = pd.concat([df_wtDUC, df_wtDUS])

        df_3 = df_2[df_2['Computer Name'].str.contains('AOR|CITHD|LOCALIT|MININT|localit|Localit|cithd|minint|aor|Aor|Minint')==False]  #remove *(AOR,Mininit,CITHD,Localit)



        df_4 = df_3[df_3['Operating System'].str.contains('Server')==True] # filter for server to get outdated servers
        df_5 = df_4[df_4['Group Name'].str.contains('LI Servers|Telco Devices|Telco RAN')==True] # To get the only LI , Telco and Telcoran devices
        outdated_server = df_5[df_5['Pattern Date']<new_3] ## outdate servers (LI Servers|Telco Devices|Telco RAN)



        ######################################
        df1 = df_3

        #Bil servers
        bil = df1[df1['Operating System'].str.contains("Server")==True]
        bil = bil.drop(['Group Name'], axis=1)



        #all client
        all_client = df1[df1['Operating System'].str.contains("Server")==False]
        all_client_a = all_client.drop(['Group Name'], axis=1)



        #online office
        onli_office = all_client[all_client['Group Name'].str.contains("Remote")==False]
        onli_office = onli_office.drop(['Group Name'], axis=1)
        a = onli_office.reset_index(drop=True)
        b = a.sort_values(by=['Version'])
        new = b["Version"].str.split(" ", n = 1, expand = True)
        b["Date"]= new[0]
        b["Version"]=new[1]
        onli_office = b
        ks = onli_office[(onli_office['Date'] < new_time)]



        #computer older than 7 days
        ls = ks['Computer Name'].values.tolist()



        #all client data remove older than 7 days
        ms = all_client_a.loc[~all_client['Computer Name'].isin(ls)]


        #online office data remove older than 7 days
        ns = onli_office.loc[~onli_office['Computer Name'].isin(ls)]
        ns.loc['Version'] =   ns['Date']+ ' ' + ns['Version']
        ns = ns.drop(['Date'], axis=1)

        ns.set_index(['Computer Name'], inplace=True)
        ms.set_index(['Computer Name'], inplace=True)
        bil.set_index(['Computer Name'], inplace=True)




        # Write each dataframe to a different worksheet.        
        name = ""
        for l in filename:
            if l == ".":
                break            
            else:
                name += l
        print("\nFilepath code: ",filepath)
        print("Filename code: ",filename)
        print("Name code: ",name)
        writer = pd.ExcelWriter(f'/home/dunfred/Documents/Web_new/Aditya File Processing System/myapp/Final Output/{name} modified.xlsx', engine='openpyxl')

        df1.to_excel(writer, sheet_name='Raw_Dump')
        bil.to_excel(writer, sheet_name='Airtel Server')
        #ms.to_excel(writer, sheet_name='All_Client')
        #ns.to_excel(writer, sheet_name='Online_Office')
        outdated_server.to_excel(writer, sheet_name='Outdated Servers')


        #########################Count for Online Office###################################

        n_7 = n_1 -timedelta(days=8)
        new_7 = n_7.strftime('%Y-%m-%d')
        n_30 = n_1 -timedelta(days=30)
        new_30 = n_30.strftime('%Y-%m-%d')
        n_3 = n_1-timedelta(days=3)
        new_3 = n_3.strftime('%Y-%m-%d')

        tm = ns.groupby(['Version'], as_index=False).count()
        tk = tm["Version"].str.split(" ", n = 1, expand = True)
        new = tk[0]
        tm['Date'] = new
        tm_new = tm.drop(['Version', 'IP Address1', 'Operating System'], axis=1)



        curr_t = n_1 - timedelta(days=0)
        curr_t = curr_t.strftime('%Y-%m-%d')
        hr_24 = tm_new[(tm_new['Date'] == curr_t)]
        day_7 = tm_new[(tm_new['Date'] > new_7)]
        day_30= tm_new[(tm_new['Date'] >  new_30)]


        hr_24_client = hr_24['Current User'].sum()
        day_30_client = day_30['Current User'].sum()
        day_7_client = day_7['Current User'].sum()




        #reg_client = '1830'
        #all_client_count = len(ms.index)
        #office_client_count = len(ns.index)


        ####################################Server Count############################

        #bil_coutn = len(bil.index)
        #reg_servers = '132'
        #env = 'production&Test'



        tm_bill = bil.groupby(['Version'], as_index=False).count()
        tk_bill = tm_bill["Version"].str.split(" ", n = 1, expand = True)
        new_bill = tk_bill[0]
        tm_bill['Date'] = new_bill
        tm_new_bill = tm_bill.drop(['Version', 'IP Address1', 'Operating System'], axis=1)


        hr_24_bill = tm_new_bill[(tm_new_bill['Date'] == curr_t)]
        day_3_bill = tm_new_bill[(tm_new_bill['Date'] > new_3)]
        day_7_bill = tm_new_bill[(tm_new_bill['Date'] > new_7)]
        day_30_bill= tm_new_bill[(tm_new_bill['Date'] >  new_30)]


        hr_24_bill = hr_24_bill['Current User'].sum()
        day_3_bill = day_3_bill['Current User'].sum()
        day_7_bill = day_7_bill['Current User'].sum()
        day_30_bill = day_30_bill['Current User'].sum()






        servers = {'Total Number of Servers Live':day_30_bill,
        'Number of Servers not updated with signature in more than 24 Hour':hr_24_bill,
        'Number of Servers not updated with signature in more than 3 days':day_3_bill,
        'Number of Servers updated with Pattern files released not more than 7 Days':day_7_bill,
        'Number of Servers not updated with signature in more than 30 days':day_30_bill}

        client = {'Total Number of Host machines Live':day_30_client,
        'Number of  Host machines not updated with signature in more than 24 Hour':hr_24_client,
        'Number of Host machines updated with Pattern files released not more than 7 Days':day_7_client,
        'Number of  Host machines not updated with signature in more than 30 days':day_30_client}




        count = pd.DataFrame([servers,client])





        count.to_excel(writer, sheet_name='Count')

        server = bil[bil['Pattern Date']<new_3]


        server = server[['IP Address1','Version','Operating System']]

        server.to_excel(writer, sheet_name='Offline Server')

        server = bil[bil['Pattern Date']<new_3]

        server = server[['IP Address1','Version','Operating System']]

        writer.save()
        print("Done")

#filename = r'myapp/static/File Processing/Raw data/Airtel.csv'
#Airtel_AV_Dashboard(filename).process()

