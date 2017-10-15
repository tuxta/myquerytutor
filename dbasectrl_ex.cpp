#include "dbasectrl_ex.h"

#include <QSqlRecord>
#include <QVector>
#include <QSqlError>
#include <QSqlField>

DbaseCtrl_Ex::DbaseCtrl_Ex(AppSettings *appSettings, QObject *parent) : QObject(parent)
{
    this->appSettings = appSettings;
    this->dbaseName = appSettings->getExDbName();
    qWarning() << "EX DBase name is " << this->dbaseName;
}

bool DbaseCtrl_Ex::connect()
{
    dbase.close();
    dbase = QSqlDatabase::addDatabase("QSQLITE", dbaseName);
    QFileInfo fileInfo(appSettings->getDbPath() + QDir::separator() + dbaseName);

    qWarning() << dbaseName;

    dbase.setConnectOptions("QSQLITE_BUSY_TIMEOUT=1");
    dbase.setDatabaseName(fileInfo.absoluteFilePath());

    if(!dbase.open())
    {
        qWarning() << "Could not open Database";
        return false;
    }

    return true;
}

bool DbaseCtrl_Ex::isOpen()
{
    return this->dbase.isOpen();
}

QVector<QVector<QString>> DbaseCtrl_Ex::runQuery(QString queryString)
{
    QVector< QVector<QString> > queryResult;
    QSqlQuery query(this->dbase);

    if(!query.exec(queryString)){
        QString errorString = query.lastError().text();
        QVector<QString> errorVec;
        errorVec.push_back(errorString);
        queryResult.push_back(errorVec);
        return queryResult;
    }
    else
    {
        int i = 0;
        QSqlRecord record;
        while(query.next())
        {
            record = query.record();
            int colCount = record.count();
            queryResult.push_back(QVector<QString>());
            for(int j = 0; j < colCount; ++j){
                queryResult[i].push_back(record.value(j).toString());
                qWarning() << queryResult[i].last();
            }
            i++;
        }
        query.previous();
        record = query.record();
        QVector<QString> cols;
        for(int index = 0; index < i; ++index){
            cols.push_back(record.field(index).name());
        }
        queryResult.push_front(cols);
    }
    return queryResult;
}
