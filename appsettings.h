#ifndef APPSETTINGS_H
#define APPSETTINGS_H

#include <QObject>
#include <QSettings>

#define ORGNAME "MyQueryTutor"
#define APPNAME "MyQueryTutor"

/**
  * Class to read and write application settings
  * to the app configuration file which is stored
  * in a platform independent way.
  */
class AppSettings : public QObject
{
    Q_OBJECT

    QSettings *settings;

public:
    explicit AppSettings(QObject *parent = 0);
    ~AppSettings();

    bool hasAppDbSet();
    bool hasExDbSet();
    QString getAppDbName();
    QString getExDbName();
    QString getDbPath();

    QByteArray getGeometry();
    QString getOrgName();

    void setAppDbName(const QString &dbName);
    void setExDbName(const QString &dbName);
    void setDbPath(const QString &dbPath);

    void setGeometry(const QByteArray &byteArray);
    void setOrgName(const QString &orgName);

    bool hasDbaseSettings();

    void write();
};

#endif // APPSETTINGS_H
