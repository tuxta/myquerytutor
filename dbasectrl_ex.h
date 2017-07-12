#ifndef DBASECTRL_EX_H
#define DBASECTRL_EX_H

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

class DbaseCtrl_Ex : public QObject
{
    Q_OBJECT

    QString dbaseName;
    QSqlDatabase dbase;
    AppSettings *appSettings;

public:
    explicit DbaseCtrl_Ex(AppSettings *appSettings, QObject *parent = 0);

    bool connect();
    bool isOpen();

    QVector<QVector<QString>> runQuery(QString queryString);
};

#endif // DBASECTRL_EX_H
