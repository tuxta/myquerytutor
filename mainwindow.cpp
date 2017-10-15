#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    this->appSettings = new AppSettings(this);
    this->dbaseCtrl_App = new DbaseCtrl_App(this->appSettings, this);
    this->dbaseCtrl_Ex = new DbaseCtrl_Ex(this->appSettings, this);
    initChecks();
    ui->setupUi(this);
    buildSelectionTree();
    restoreGeometry(appSettings->getGeometry());
}

void MainWindow::initChecks()
{
    // Check to see if this is the first time the program
    // has been run. If so write the setting file
    if(!appSettings->hasDbaseSettings()) {
        this->appSettings->setOrgName("MyQueryTutor");
        this->appSettings->setAppDbName("MQT_APP.sqlite");
        this->appSettings->setExDbName("MQT_EX.sqlite");
        this->appSettings->setDbPath(QStandardPaths::writableLocation(QStandardPaths::DataLocation));
        this->appSettings->write();

    }

    this->dbaseCtrl_App->connect();

    if(!dbaseCtrl_App->isOpen())
    {
        qWarning() << "Cannot connect to Database, now exiting";

        QMessageBox::critical(0,"Database Connect",
                       "Could not connect to Database!\n"
                       "Please check your settings");
        exit(0);
    }

    this->dbaseCtrl_Ex->connect();

    if(!dbaseCtrl_Ex->isOpen())
    {
        qWarning() << "Cannot connect to Database, now exiting";

        QMessageBox::critical(0,"Database Connect",
                       "Could not connect to Database!\n"
                       "Please check your settings");
        exit(0);
    }

}

void MainWindow::buildSelectionTree()
{
    ui->questionSelectTree->setColumnCount(1);
    ui->questionSelectTree->header()->close();

    QMap<std::string, std::vector<std::string>> treeItems = dbaseCtrl_App->getQuestionList();

    QList<std::string> keys = treeItems.keys();
    for(QList<std::string>::iterator currKey = keys.begin();
        currKey != keys.end(); currKey++)
    {
        QTreeWidgetItem *topicItem = this->addRootItemToTree(QString::fromStdString(*currKey));

        std::vector<std::string> questions = treeItems[*currKey];
        for(std::vector<std::string>::iterator iter = questions.begin(); iter != questions.end(); iter++)
        {
            addChildItemToTree(topicItem, QString::fromStdString(*iter));
        }
    }
}

QTreeWidgetItem* MainWindow::addRootItemToTree(QString title)
{
    QTreeWidgetItem *item = new QTreeWidgetItem(ui->questionSelectTree);
    item->setText(0, title);

    return item;

}

void MainWindow::addChildItemToTree(QTreeWidgetItem *parent, QString title)
{
    QTreeWidgetItem *item = new QTreeWidgetItem(parent);
    item->setText(0, title);
}

MainWindow::~MainWindow()
{
    delete appSettings;
    delete dbaseCtrl_App;
    delete dbaseCtrl_Ex;
    delete ui;
}

void MainWindow::on_expectedResult_button_clicked()
{
    // Get the exemplar query for the current question
    QString query = this->dbaseCtrl_App->getQuestionQuery(this->topic, this->question);
    qWarning() << query;

    // Run the query on the exercises data base
    //QVector<QVector<QString>> result = this->dbaseCtrl_Ex->runQuery(query);

    // Display the result

}
void MainWindow::on_runQuery_button_clicked()
{
    QVector<QVector<QString>> result = this->dbaseCtrl_Ex->runQuery(ui->queryTextArea->toPlainText());

    int columns = result[1].length();
    int rows = result.length();

    qWarning() << "Colums " << columns;
    qWarning() << "Rows " << rows;

    ui->resultsTable->setColumnCount(columns);
    ui->resultsTable->setRowCount(rows - 1);

    ui->resultsTable->clear();

    QStringList headerLabels;
    for(int i = 0; i < columns; ++i){
        headerLabels << result[0][i];
    }
    ui->resultsTable->setHorizontalHeaderLabels(headerLabels);

    // Create and populate a table with the result
    QTableWidgetItem *cell;
    for(int i = 1; i < rows; ++i){
        for(int j = 0; j < columns; ++j){
            cell = new QTableWidgetItem;
            cell->setText(result[i][j]);
            ui->resultsTable->setItem(i - 1, j, cell);
        }
    }
}

void MainWindow::on_tableData_button_clicked()
{

}

void MainWindow::on_help_button_clicked()
{

}

void MainWindow::closeEvent(QCloseEvent *event)
 {
     appSettings->setGeometry(this->saveGeometry());
     QWidget::closeEvent(event);
 }

void MainWindow::on_questionSelectTree_clicked(const QModelIndex &index)
{
    if(index.parent().isValid()) {
        QModelIndex topicItem = index.parent();

        this->question = index.data(0).toString();
        this->topic = topicItem.data(0).toString();

        QString description = dbaseCtrl_App->getQuestion(this->topic, this->question);

        if(description != NULL)
            ui->questionTextArea->setText(description);

        ui->resultsTable->clear();

        // For now, clearing the query
        // In future, reload previous query if exists
        ui->queryTextArea->setText("");


    }
}
