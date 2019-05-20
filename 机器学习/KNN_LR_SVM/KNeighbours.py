# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:56:09 2019

只支持二分类

@author: Season
"""
#测试代码
#import numpy as np
#mdata = pd.read_csv("C://testdata//420testdata.csv",encoding = "gbk")
#mdata = mdata[['住院天数', '年龄','咳嗽', '流涕', '呼吸音粗','性别']]
#mdata.dropna(axis = 0, how = 'any', inplace = True)
#vars_c = ['住院天数', '年龄']
#vars_d = ['咳嗽', '流涕', '呼吸音粗']
#target = ['性别']
#testdata=None
#n_neighbors = 6
#KNN(mdata, target, vars_c, vars_d, testdata=None,n_neighbors=5)

# In[]
def KNN(mdata, target, vars_c, vars_d, testdata=None, n_neighbors = 6):
    
    import numpy as np
    import pandas as pd
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split
    import sklearn.metrics as metrics
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from sklearn import preprocessing
    
    '''
    :param mdata: 源数据
    :param target: 结局变量名Y
    :param vars_c: 连续变量名集合X
    :param vars_d: 分类变量名集合X
    :param testdata: 待预测数据
    '''
    
    '''
    数据校验
    判断传入X的连续变量和分类变量格式是否合格，是否含有空值
    '''
    for var_c in vars_c:
        if type(mdata[var_c].loc[0]) not in [int,float,np.int64,np.float64]:
            return("错误:变量%s不是定量变量，请重新选择" %var_c)
        if mdata[var_c].isna().any() :
            return("错误:变量%s含有空值，请重新选择" %var_c)
    for var_d in vars_d:
        if type(mdata[var_d].loc[0]) not in [str,bool,int]:
            return("错误:变量%s不是定性变量, 请重新选择" %var_d)
        if mdata[var_d].isna().any() == True:
            return("错误:变量%s含有空值，请重新选择" %var_c)
    if mdata[target[0]].isna().any() == True:
        return("错误:结局变量%s含有空值，请重新选择" %target)
    if len(set(mdata[target].iloc[:,0])) > 2:
        return("错误:结局变量类别数量大于2，目前只支持2分类的建模")
    #print("--------模型数据校验完毕,开始模型训练---------")
    
    '''
    先对数据进行预处理：
    1）对连续性变量做极差标准化处理
    2) 目标变量若是字符型或者是逻辑性，转化成0,1
    3）对分类变量X进行转化
    转化之后建立模型，数据将分为两部分，一部分作为训练集，一部分作为测试集
    使用训练集进行模型训练，测试集作为模型评估测试，模型建立完成后使用待预测数据testdata进行预测
    '''
    
    #极差标准化处理
    min_max_scaler = preprocessing.MinMaxScaler()
    for var_c in vars_c:
        mdata[var_c] = min_max_scaler.fit_transform(np.array(mdata[var_c].astype(np.float64)).reshape(-1,1))            
    
    if type(mdata[target].iloc[0,0]) in [str,bool]:
        target_dummy = pd.get_dummies(mdata[target],prefix = target ,prefix_sep = "-").iloc[:,1].to_frame()
        new_target = target_dummy.columns.values.tolist()
        mdata = pd.concat([mdata,target_dummy],axis = 1)
        mdata = mdata.drop(target,axis = 1)
        target = new_target
        
    "对训练数据集和待预测数据集的分类变量都进行创建哑变量操作，创建成功之后删除原变量"
    for var_d in vars_d:
        dummies = pd.get_dummies(mdata.loc[:,var_d],prefix = var_d, prefix_sep = "-")
        mdata = pd.concat([mdata,dummies],axis=1) 
    mdata = mdata.drop(vars_d,axis = 1)
           
    
    #对测试数据集进行处理：
    if testdata != None:
        for var_c in vars_c:
            testdata[var_c] = min_max_scaler.fit_transform(np.array(testdata[var_c].astype(np.float64)).reshape(-1,1))
        for var_d in vars_d:
            test_dummies = pd.get_dummies(testdata.loc[:,var_d],prefix = var_d, prefix_sep = "-")
            testdata = pd.concat([test_dummies,testdata],axis=1)
        testdata = testdata.drop(vars_d,axis = 1)
    
    '''
    设置KNN模型超参数，若没有可自行添加：
    n_neighbors : 近邻个数
    '''
    clf = KNeighborsClassifier(n_neighbors = n_neighbors) #默认为欧式距离
    
    "设置训练集集和测试集"
    x_train, x_test, y_train, y_test = train_test_split(mdata.drop(target,axis=1),
                                                        mdata[target].astype(int),test_size = 0.3)
    
    clf.fit(x_train,y_train.values.ravel())
    prediction = clf.predict(x_test)
    pred_score = metrics.accuracy_score(prediction,y_test)
    fpr_test, tpr_test, th_test = metrics.roc_curve(y_test, prediction)
    auc_score = metrics.auc(fpr_test, tpr_test)
    
    "输出内容1：直接以字符串方式输出结果"
    Output_Msg = ("KNN模型构建成功:模型准确度为%.4f,模型AUC评分为%.4f" %(pred_score,auc_score))
    #print("KNN模型构建成功:模型准确度为%.4f,模型AUC评分为%.4f" %(pred_score,auc_score))
    
    "输出内容2：图2"
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    "绘制模型ROC曲线"
    pred_y_train_p = clf.predict_proba(x_train)[:,1]
    pred_y_test_p = clf.predict_proba(x_test)[:,1]
    
    fpr_train, tpr_train, th_train = metrics.roc_curve(y_train, pred_y_train_p)
    fpr_test, tpr_test, th_test = metrics.roc_curve(y_test, pred_y_test_p)
    
    plt.figure(figsize=[6,6])
    plt.plot(fpr_test, tpr_test, color='b')
    plt.plot(fpr_train, tpr_train, color='r')
    plt.title('ROC曲线')
    save_path = "./Roc_curve.jpg"
    plt.savefig("./Roc_curve.jpg")
    plt.show()
    
    "输出结果3：若存在测试数据集，则输出数据框dataframe"
    if testdata != None:
        testdata_pred = pd.DataFrame(clf.predict(testdata).tolist(),columns = target)
        testdata = pd.concat([testdata_pred,testdata],axis = 1)
        
    # 多个结果封装成字典形式
    rlt = {"Output_Msg":Output_Msg,
           "Roc_curve":save_path,
           "test_rlt":testdata}
    return rlt