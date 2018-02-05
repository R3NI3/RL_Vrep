import torch
from torch.autograd import Variable
import numpy as np
import os
import pandas


def getDataLoaderFromList(listPath='data/demo.csv', batch_sz=3):
    """
        Get Data Loader From List with the follow format 
            
        First Line: metadata column 
            ID_VIDEO, TIME_STAMP, ID_ROBOS
        
        Second Line:
            metadata
            
        Third Line:
            #To Do
        
        Fourth and on:
            	- x; y; theta (x1 team 1) #demo
            	- x; y; theta (x1 team 2) #demo
            	- x; y (ball)
            
        
        Keyword arguments
        _________________
        
            listPath (str) :
                dir for the csv file (default: "data/demo.csv")
                
            batch_sz (int) :
                size of batch (default: 3)
               
    """    
    
    dataset = pandas.read_csv(listPath, sep=';')
    
    listInfo = dataset.iloc[0:1, :]  
    # soon will be used to get the matadata of the file
    positionInfo = dataset.iloc[2:, :]
    positionInfo.columns = dataset.iloc[1,:]
    values = np.array(positionInfo.iloc[:,:].values, dtype=np.float32)
    
    train_loader = torch.utils.data.DataLoader(dataset=values,
                                           batch_size=batch_sz,
                                           shuffle=True)
    
    return train_loader
         
if __name__ == '__main__':
    train_loader = getDataLoaderFromList()
    
    for i, pos in enumerate(train_loader):

        pos = Variable(pos)
        print (pos)
