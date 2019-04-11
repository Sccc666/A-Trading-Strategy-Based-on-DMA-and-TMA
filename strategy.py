import numpy as np

asset_index = 1 # only consider BTC (the **second** crypto currency in dataset)
short_length = 20
median_length = 50
long_length = 150

def handle_bar(counter,  # a counter for number of minute bars that have already been tested
               time,  # current time in string format such as "2018-07-30 00:30:00"
               data,  # data for current minute bar (in format 2)
               init_cash,  # your initial cash, a constant
               transaction,  # transaction ratio, a constant
               cash_balance,  # your cash balance at current minute
               crypto_balance,  # your crpyto currency balance at current minute
               total_balance,  # your total balance at current minute
               position_current,  # your position for 4 crypto currencies at this minute
               memory 
               ):
    ML = 0 #initialization
    MS = 0
    MM = 0
    
    position_new = position_current   # Get position of last minute
   
   
    if 'a' in dir(memory):
        memory.a.append(data[asset_index,1])
    else:
        class media:
            a=[] #Close price
            lastp=0. #last position
        memory=media()
        memory.a.append(data[asset_index,1])

    
    if counter>=20:
        MS = np.mean(memory.a[counter-short_length:counter]) #Calculate the 20-day moving average
        ML = np.mean(memory.a[counter-long_length:counter])  #Calculate the 150-day moving average
        MM = np.mean(memory.a[counter-median_length:counter]) #Calculate the 50-day moving average
        #RDV = MS - ML #Daily deviation value
        
    if (counter % short_length == 0):      #Check the price every 20 minutes to see if the price meets the conditions of long or short
    
        #Long signal: The short-term moving average is higher than the long-term moving average and exceeds SD points
        if memory.lastp == 0:
            if MS > ML and MM > ML :   
                position_new[asset_index] += 5
                memory.lastp=position_new[asset_index]
                
        if memory.lastp > 0:
            if MS > ML and MM < ML :   
                position_new[asset_index] -= 10
                memory.lastp=position_new[asset_index]
        
        if memory.lastp == 0:
            if MS < ML and MM < ML : 
                position_new[asset_index] -= 5
                memory.lastp=position_new[asset_index]
                
        if memory.lastp < 0:
            if MS < ML and MM > ML : 
                position_new[asset_index] += 10
                memory.lastp=position_new[asset_index]
        
        
    return position_new,memory


