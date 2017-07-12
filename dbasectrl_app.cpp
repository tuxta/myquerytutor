#include "dbasectrl_app.h"
#include <vector>
#include <string>



DbaseCtrl_App::DbaseCtrl_App(AppSettings *appSettings, QObject *parent) : QObject(parent)
{

    this->appSettings = appSettings;
    this->dbaseName = appSettings->getAppDbName();
}

bool DbaseCtrl_App::connect()
{
    qWarning() << "Now in connect APP function";

    dbase.close();
    dbase = QSqlDatabase::addDatabase("QSQLITE", this->dbaseName);
    QFileInfo fileInfo(appSettings->getDbPath() + QDir::separator() + this->dbaseName);

    qWarning() << this->dbaseName;

    dbase.setConnectOptions("QSQLITE_BUSY_TIMEOUT=1");
    dbase.setDatabaseName(fileInfo.absoluteFilePath());

    if(!dbase.open())
    {
        qWarning() << "Could not open Database";
        return false;
    }
    qWarning() << "Database should be open";

    return true;

}

bool DbaseCtrl_App::isOpen()
{
    return this->dbase.isOpen();
}

QMap<std::string, std::vector<std::string>> DbaseCtrl_App::getQuestionList()
{
    QMap<std::string, std::vector<std::string>> questionList;

    QSqlQuery query(this->dbase);

    query.prepare("SELECT Topic.name, Question.title "
                  "FROM Topic, Question "
                  "WHERE Question.topicId = Topic.id ");

    if(!query.exec())
        qWarning("Could not run query");
    else
    {
        // Load each Topic into the questionList
        while(query.next())
        {
            std::string key = query.value(0).toString().toStdString();
            std::string value = query.value(1).toString().toStdString();

            //Add record to container
            if(questionList.contains(key)) {
                std::vector<std::string> valVect;
                valVect.push_back(value);
                questionList.insert(key, valVect);
            } else {
                questionList[key].push_back(value);
            }
        }
    }

    return questionList;
}

QString DbaseCtrl_App::getQuestion(QString topic, QString question)
{
    QSqlQuery query(this->dbase);

    query.prepare("SELECT description "
                  "FROM Topic, Question "
                  "WHERE Question.topicId = Topic.id "
                  "AND Topic.name = '" + topic + "'"
                  "AND Question.title = '" + question + "'"
                  );

    if(!query.exec()) {
        qWarning("Could not run query");
        return NULL;
    } else {
        query.next();
        return query.value(0).toString();
    }

}

QString DbaseCtrl_App::getQuestionQuery(QString topic, QString question)
{
    QSqlQuery query(this->dbase);

    query.prepare("SELECT Question.resultQuery "
                  "FROM Topic, Question "
                  "WHERE Question.topicId = Topic.id "
                  "AND Topic.name = '" + topic + "'"
                  "AND Question.title = '" + question + "'"
                  );

    if(!query.exec()) {
        qWarning("Could not run query");
        return NULL;
    } else {
        query.next();
        return query.value(0).toString();
    }
}
