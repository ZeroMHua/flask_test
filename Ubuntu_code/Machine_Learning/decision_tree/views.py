from . import DST_blue

@DST_blue.route("/DST",methods=['POST'])
def DSTS():
    import numpy as np
    import pandas as pd
    from flask import request
    from flask import jsonify
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    import sklearn.metrics as metrics
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import sklearn.tree as tree
    import graphviz

    data = request.json
    filename = data['data'][0]["filename"]
    # testdata = data['data'][0]["testdata"]
    testdata = None
    graph_show = False
    # n_neighbors = data['data'][0]["n_neighbors"]
    tab_list = data['data'][1]["tab_list"]
    vars_c = data['data'][1]["vars_c"]
    vars_d = data['data'][1]["vars_d"]
    target = data['data'][1]["target"]
    mdata = pd.read_csv(filename, encoding="gbk")
    mdata = mdata[tab_list]
    mdata.dropna(axis=0, how='any', inplace=True)

    '''
        先对数据进行预处理：
        1）目标变量若是字符型或者是逻辑性，转化成0,1
        2）对分类变量X进行转化
        转化之后建立模型，数据将分为两部分，一部分作为训练集，一部分作为测试集
        使用训练集进行模型训练，测试集作为模型评估测试，模型建立完成后使用待预测数据testdata进行预测
        '''
    if type(mdata[target].iloc[0, 0]) in [str, bool]:
        target_dummy = pd.get_dummies(mdata[target], prefix=target, prefix_sep="-").iloc[:, 1].to_frame()
        new_target = target_dummy.columns.values.tolist()
        mdata = pd.concat([mdata, target_dummy], axis=1)

    "对训练数据集和待预测数据集的分类变量都进行创建哑变量操作，创建成功之后删除原变量"
    for var_d in vars_d:
        dummies = pd.get_dummies(mdata.loc[:, var_d], prefix=var_d, prefix_sep="-")
        mdata = pd.concat([mdata, dummies], axis=1)
        if testdata != None:
            test_dummies = pd.get_dummies(testdata.loc[:, var_d], prefix=var_d, prefix_sep="-")
            testdata = pd.concat([test_dummies, testdata], axis=1)

    mdata = mdata.drop(vars_d, axis=1)
    mdata = mdata.drop(target, axis=1)
    if testdata != None:
        testdata = testdata.drop(vars_d, axis=1)
    target = new_target

    clf = DecisionTreeClassifier(criterion='gini')

    x_train, x_test, y_train, y_test = train_test_split(mdata.drop(target, axis=1),
                                                        mdata[target].astype(int), test_size=0.3)

    clf.fit(x_train, y_train)
    prediction = clf.predict(x_test)
    pred_score = metrics.accuracy_score(prediction, y_test)
    fpr_test, tpr_test, th_test = metrics.roc_curve(y_test, prediction)
    auc_score = metrics.auc(fpr_test, tpr_test)

    "输出内容1：直接以字符串方式输出结果"
    Output_Msg = ("决策树模型构建成功:模型准确度为%.4f,模型AUC评分为%.4f" % (pred_score, auc_score))
    # print("决策树模型构建成功:模型准确度为%.4f,模型AUC评分为%.4f" %(pred_score,auc_score))

    "输出内容2：图1"
    "绘制模型变量重要性柱状图"
    importance = sorted(clf.feature_importances_, reverse=True)
    features = x_train.columns
    idx = np.argsort(importance)[::1]
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.title(r'模型变量重要性图解')
    color = cm.jet(np.array(importance) / max(importance))
    plt.barh(idx, importance, color=color)
    plt.yticks(idx, features)
    plt.grid(axis="x")
    save_path1 = "./feature_importance.png"
    plt.savefig("./feature_importance.png")
    # plt.show()

    "输出内容3：图2"
    "绘制模型ROC曲线"
    pred_y_train_p = clf.predict_proba(x_train)[:, 1]
    pred_y_test_p = clf.predict_proba(x_test)[:, 1]

    fpr_train, tpr_train, th_train = metrics.roc_curve(y_train, pred_y_train_p)
    fpr_test, tpr_test, th_test = metrics.roc_curve(y_test, pred_y_test_p)

    plt.figure(figsize=[6, 6])
    plt.plot(fpr_test, tpr_test, color='b')
    plt.plot(fpr_train, tpr_train, color='r')
    plt.title('ROC曲线')
    save_path2 = "./Roc_curve.png"
    plt.savefig("./Roc_curve.png")
    # plt.show()

    "输出内容4：决策树图形，注意，若决策树过于复杂，不建议输出"
    save_path3 = None
    if graph_show:
        dot_data = tree.export_graphviz(clf, out_file=None, feature_names=x_train.columns,
                                        class_names=['0', '1'], filled=True)
        dot_data = dot_data[:21] + 'fontname = "FangSong",' + dot_data[21:]
        graph = graphviz.Source(dot_data)
        graph.render('./tree', format='png')
        save_path3 = "./tree.png"

    "输出结果5：若存在测试数据集，则输出数据框dataframe"
    if testdata != None:
        testdata_pred = pd.DataFrame(clf.predict(testdata).tolist(), columns=target)
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
    for i in range(3):
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
        if i ==0:

            name = "模型变量重要性图解"
            pic["title"] = name
            pic['path'] = save_path1
            pic_list.append(pic)
        elif i == 1:
            name = "ROC曲线图"
            pic["title"] = name
            pic['path'] = save_path2
            pic_list.append(pic)
        elif i == 2:
            name = "决策树图"
            pic["title"] = name
            pic['path'] = save_path3
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
           "feature_importance": save_path1,
           "Roc_curve": save_path2,
           "tree_png": save_path3,
           "test_rlt": testdata}
    return jsonify(yy=aq)

