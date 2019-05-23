from . import SVM_blue

@SVM_blue.route("/SVM",methods=['POST'])
def SVMS():
    import numpy as np
    import pandas as pd
    from flask import request
    from flask import jsonify
    from sklearn.svm import SVC
    from sklearn.model_selection import train_test_split
    import sklearn.metrics as metrics
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from sklearn import preprocessing
    data = request.json
    filename = data['data'][0]["filename"]
    testdata = None
    kernel = data['data'][0]["kernel"]
    C = data['data'][0]["C"]
    gamma = data['data'][0]["gamma"]
    # testdata = data['data'][0]["testdata"]
    testdata = None
    # n_neighbors = data['data'][0]["n_neighbors"]
    tab_list = data['data'][1]["tab_list"]
    vars_c = data['data'][1]["vars_c"]
    vars_d = data['data'][1]["vars_d"]
    target = data['data'][1]["target"]
    mdata = pd.read_csv(filename, encoding="gbk")
    mdata = mdata[tab_list]
    mdata.dropna(axis=0, how='any', inplace=True)
    mdata = mdata.iloc[0:1000,:]

    '''
        先对数据进行预处理：
        1）对连续性变量做极差标准化处理
        2) 目标变量若是字符型或者是逻辑性，转化成0,1
        3）对分类变量X进行转化
        转化之后建立模型，数据将分为两部分，一部分作为训练集，一部分作为测试集
        使用训练集进行模型训练，测试集作为模型评估测试，模型建立完成后使用待预测数据testdata进行预测
        '''

    # 极差标准化处理
    min_max_scaler = preprocessing.MinMaxScaler()
    for var_c in vars_c:
        mdata[var_c] = min_max_scaler.fit_transform(np.array(mdata[var_c].astype(np.float64)).reshape(-1, 1))

    if type(mdata[target].iloc[0, 0]) in [str, bool]:
        target_dummy = pd.get_dummies(mdata[target], prefix=target, prefix_sep="-").iloc[:, 1].to_frame()
        new_target = target_dummy.columns.values.tolist()
        mdata = pd.concat([mdata, target_dummy], axis=1)
        mdata = mdata.drop(target, axis=1)
        target = new_target

    "对训练数据集和待预测数据集的分类变量都进行创建哑变量操作，创建成功之后删除原变量"
    for var_d in vars_d:
        dummies = pd.get_dummies(mdata.loc[:, var_d], prefix=var_d, prefix_sep="-")
        mdata = pd.concat([mdata, dummies], axis=1)
    mdata = mdata.drop(vars_d, axis=1)

    # 对测试数据集进行处理：
    if testdata != None:
        for var_c in vars_c:
            testdata[var_c] = min_max_scaler.fit_transform(np.array(testdata[var_c].astype(np.float64)).reshape(-1, 1))
        for var_d in vars_d:
            test_dummies = pd.get_dummies(testdata.loc[:, var_d], prefix=var_d, prefix_sep="-")
            testdata = pd.concat([test_dummies, testdata], axis=1)
        testdata = testdata.drop(vars_d, axis=1)

    '''
    设置SVM模型超参数，若没有可自行添加：
    kernel : 核函数,可选 "linear" or "rbf"
    gamma : 0 < gamma < 1
    C : 惩罚系数 0 < C < 1
    '''
    clf = SVC(kernel=kernel, C=C, gamma=gamma, probability=True)

    "设置训练集集和测试集"
    x_train, x_test, y_train, y_test = train_test_split(mdata.drop(target, axis=1),
                                                        mdata[target].astype(int), test_size=0.3)

    clf.fit(x_train, y_train)
    prediction = clf.predict(x_test)
    pred_score = metrics.accuracy_score(prediction, y_test)
    fpr_test, tpr_test, th_test = metrics.roc_curve(y_test, prediction)
    auc_score = metrics.auc(fpr_test, tpr_test)

    "输出内容1：直接以字符串方式输出结果"
    Output_Msg = ("SVM模型构建成功:模型准确度为%.4f,模型AUC评分为%.4f" % (pred_score, auc_score))
    # print("SVM模型构建成功:模型准确度为%.4f,模型AUC评分为%.4f" %(pred_score,auc_score))

    "输出内容2：图2"
    "绘制模型ROC曲线"
    pred_y_train_p = clf.predict_proba(x_train)[:, 1]
    pred_y_test_p = clf.predict_proba(x_test)[:, 1]

    fpr_train, tpr_train, th_train = metrics.roc_curve(y_train, pred_y_train_p)
    fpr_test, tpr_test, th_test = metrics.roc_curve(y_test, pred_y_test_p)

    plt.figure(figsize=[6, 6])
    plt.plot(fpr_test, tpr_test, color='b')
    plt.plot(fpr_train, tpr_train, color='r')
    plt.title('ROC曲线')
    save_path = "./Roc_curve.png"
    plt.savefig("./Roc_curve.png")
    # plt.show()

    "输出结果3：若存在测试数据集，则输出数据框dataframe"
    if testdata != None:
        testdata_pred = pd.DataFrame(clf.predict(testdata).tolist(),                   columns=target)
        testdata = pd.concat([testdata_pred, testdata], axis=1)

    a = {"parentTitle": "",
         "parentContent": [],
         "title": "",
         "content": [],
         "rowTop": "",
         "colTop": "",
         "rowNames": [1],
         "combination": False,
         "colNames": ['模型准确度', '模型AUC评分'],
         "values": []
         }
    a["values"].append(str(pred_score)[0:6])
    a["values"].append(str(auc_score)[0:6])
    pic_list = []
    pic = {
        "parentTitle": "",
        "title": "",
        "type": ".png",
        "path": "",
        "dependPath": "",
        "content": [{}],
        "params": {},
        "reload": False
    }
    name = "SVM"
    pic["title"] = name
    pic['path'] = save_path
    pic_list.append(pic)
    aq = [{"code": 0,
           "message": None,
           "varInfos": None,
           "mData": None,
           "fields": [],
           "rFiles": [],
           "tables": []}]

    aq[0]["tables"].append(a)
    aq[0]["rFiles"] = pic_list

    # 多个结果封装成字典形式
    rlt = {"Output_Msg": Output_Msg,
           "Roc_curve": save_path,
           "test_rlt": testdata}
    return jsonify(yy=aq)
