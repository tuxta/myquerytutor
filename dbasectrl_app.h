#ifndef DBASECTRL_APP_H
#define DBASECTRL_APP_H

#include <QMap>
#include <QDir>
#include <string>
#include <vector>
#include <QDebug>
#include <QVector>
#include <QString>
#include <QObject>
#include <QSqlQuery>
#include <QFileInfo>
#include <QVectorIterator>
#include <QtSql/QSqlDatabase>

#include "appsettings.h"


class DbaseCtrl_App : public QObject
{
    Q_OBJECT

    QString dbaseName;
    QSqlDatabase dbase;
    AppSettings *appSettings;

public:
    explicit DbaseCtrl_App(AppSettings *appSettings, QObject *parent = 0);

    bool connect();
    bool isOpen();

    QMap<std::string, std::vector<std::string>> getQuestionList();
    QString getQuestion(QString topic, QString question);
    QString getQuestionQuery(QString topic, QString question);
};

#endif // DBASECTRL_APP_H
