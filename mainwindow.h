#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMap>
#include <vector>
#include <string>
#include <QMapIterator>
#include <QMainWindow>
#include <QMessageBox>
#include <QMapIterator>
#include <QStandardPaths>
#include <QTreeWidgetItem>
#include <QVectorIterator>
#include <QTreeWidgetItem>



#include "appsettings.h"
#include "dbasectrl_app.h"
#include "dbasectrl_ex.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

    AppSettings *appSettings;
    DbaseCtrl_App *dbaseCtrl_App;
    DbaseCtrl_Ex *dbaseCtrl_Ex;

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_expectedResult_button_clicked();
    void on_runQuery_button_clicked();
    void on_tableData_button_clicked();
    void on_help_button_clicked();

    void on_questionSelectTree_clicked(const QModelIndex &index);

private:

    QString topic;
    QString question;
    Ui::MainWindow *ui;
    void initChecks();
    void buildSelectionTree();

    QTreeWidgetItem* addRootItemToTree(QString title);
    void addChildItemToTree(QTreeWidgetItem *parent, QString name);

    void closeEvent(QCloseEvent *event);
};

#endif // MAINWINDOW_H
