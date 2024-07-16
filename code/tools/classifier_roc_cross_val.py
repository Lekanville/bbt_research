import os
import numpy as np
from loguru import logger
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay, auc, roc_curve
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score   

import tools.classifier_algorithms as class_alg

def classifier_roc_cross_val(level, classifier_name, df, OUTPUT_FOLDER):  
    #random_state = np.random.RandomState(0)

    classifier = class_alg.get_algorithm(classifier_name)

    tprs = []
    aucs = []
    accs = []
    imp = []

    mean_fpr = np.linspace(0, 1, 100)

    fig, ax = plt.subplots(figsize=(6, 6))

    for fold, data in enumerate(df):
        
        train = data[0]['train']
        test = data[1]['test']
        
        classifier.fit(train["X_train"], train["y_train"])
        viz = RocCurveDisplay.from_estimator(
            classifier,
            test["X_test"],
            test["y_test"],
            name=f"ROC fold {fold}",
            alpha=0.3,
            lw=1,
            ax=ax,
            #plot_chance_level=(fold == n_splits - 1),
        )
        
        class_pred = classifier.predict(test["X_test"])
        
        accs.append(accuracy_score(test["y_test"], class_pred))
        
        interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
        interp_tpr[0] = 0.0
        tprs.append(interp_tpr)
        aucs.append(viz.roc_auc)

        if classifier_name == "RFC":
            imp.append(classifier.feature_importances_)
        elif classifier_name == "SVM":
            imp.append(classifier.coef_[0])
        elif classifier_name == "LogReg":
            imp.append(classifier.coef_[0])


    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    ax.plot(
        mean_fpr,
        mean_tpr,
        color="b",
        #label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
        label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
        lw=2,
        alpha=0.8,
    )

    ax.plot([0,1], [0,1], ls='--')

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    ax.fill_between(
        mean_fpr,
        tprs_lower,
        tprs_upper,
        color="grey",
        alpha=0.2,
        label=r"$\pm$ 1 std. dev.",
    )

    ax.set(
        xlim=[-0.05, 1.05],
        ylim=[-0.05, 1.05],
        xlabel="False Positive Rate",
        ylabel="True Positive Rate",
        title=f"Mean ROC curve with variability-"+level+" "+classifier_name,
    )
    
    logger.info("Accuracies at each fold")
    print(accs)

    logger.info("Mean of the Fold Accuracies")
    mean_acc = np.mean(accs)
    print(mean_acc)

    #logger.info("Importances at each fold")
    #print (imp)

    mean_imp = np.mean(imp, axis=0)
    #logger.info("Mean of the Importances for the fold")
    #print (mean_imp)

    ax.axis("square")
    ax.legend(loc="lower right")
    name_and_ext = "_".join(level.split(" "))+".png"
    filename = classifier_name+"_"+ name_and_ext
    plt.savefig(os.path.join(OUTPUT_FOLDER, filename))

    return mean_imp
