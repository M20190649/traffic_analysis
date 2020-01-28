from fbprophet import Prophet


def create_model(config):
    
    
    
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=False,
        yearly_seasonality=False,
        changepoint_prior_scale=0.02,
    )
    model.add_seasonality(
        name='daily',
        period=1,
        fourier_order=16,
        prior_scale=0.1,

    )
    model.add_seasonality(
        name='weekly',
        period=7,
        fourier_order=2,
        prior_scale=0.1,
    )


def df_to_fbpro(df):
    if len(df.columns) == 1:
        df = df.reset_index()
    df.columns = ['ds', 'y']
    return df

def metrics(df_test, forecast, metric):
    
    if metric == 'smape':
        y_true = df_test['y']
        y_forecast = forecast[-n_tests:]['yhat']
        smape = ((y_true - y_forecast).abs() / (y_true.abs() + y_forecast.abs())).mean() * 200
        print('The SMAPE error is:', smape)
        return smape
    
    
### Data Cleaning

def istimecheck(time):
    timeformat = "%Y-%m-%d %H:%M:%S.%f"
    
    try:
        validtime = datetime.datetime.strptime(time, timeformat)
        return True
        #Do your logic with validtime, which is a valid format
    except ValueError:
        return False
        #Do your logic for invalid format (maybe print some message?).

def ProcessLargeTextFile():
    logging.basicConfig(filename='errors.log',level=logging.DEBUG)
    bunchsize = 1000000     # Experiment with different sizes
    bunch = []
    start = time.time()
    errors = 0
    time_errors = 0
    speed_errors = 0
    with open('/Users/bluekidds/Downloads/tn_data/IISIRoadMOE.txt', errors='replace') as r, open("IISIRoadMOE_Processed.txt", "w") as w:
        for line in r:
            line_list = line.split()
            if len(line_list) < 8:
                print('Error occur...')
                print(line_list)
                break
            
            my_time = line_list[3]+' '+line_list[4]
            

            if not istimecheck(my_time):
                #print('Error detected when extracting time')
                errors += 1
                time_errors += 1
                logging.error("Time format error:" + my_time)
                continue 
            if not line_list[5].replace('.','',1).isdigit():
                if float(line_list[7]) == -1:
                    pass
                else:
                    #print('Error detected when extracting speed')
                    errors += 1
                    speed_errors +=1
                    logging.error("Speed format error:" + line_list[5])
                    continue
                
            bunch.append(','.join([line_list[0], line_list[1],line_list[3]+' '+line_list[4], line_list[5] + '\n']))
            
            if len(bunch) == bunchsize:
                print('Processed 1 million lines in: ' + str(time.time()-start))
                print('Number of time errors accumulated: ' + str(time_errors))
                print('Number of speed errors acucmulated: ' + str(speed_errors))
                start = time.time()
                w.writelines(bunch)
                
                bunch = []
        w.writelines(bunch)
        print('Total errors: ' + str(errors) + ' and Speed variable errors ' + str(speed_errors) + ' and Time variable errors: ' + str(time_errors))
