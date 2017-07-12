#include "appsettings.h"

AppSettings::AppSettings(QObject *parent) : QObject(parent)
{
    this->settings = new QSettings(ORGNAME, APPNAME, this);
}

AppSettings::~AppSettings()
{
    delete settings;
}

/**
  * Check to see if database has already been set.
  * @returns True is database setting exits, False if not
  */
bool AppSettings::hasAppDbSet()
{
    if(settings->contains("Database/dbName"))
        return true;
    return false;
}

bool AppSettings::hasExDbSet()
{
    if(settings->contains("Database/exDbName"))
        return true;
    return false;
}

/**
  * Retrieve Database file name
  * @return QString the db file name
  */
QString AppSettings::getAppDbName()
{
    return settings->value("Database/dbName").toString();
}

QString AppSettings::getExDbName()
{
    return settings->value("Database/exDbName").toString();
}

QString AppSettings::getDbPath()
{
    return settings->value("Database/dbPath").toString();
}

void AppSettings::setDbPath(const QString &dbPath)
{
    settings->setValue("Database/dbPath", dbPath);
}



/**
  * Retrieve App geometry
  * @returns The main window size and location
  */
QByteArray AppSettings::getGeometry()
{
    return settings->value("MainWindow/geometry").toByteArray();
}

/**
  * Retrieve the Organisation Name
  * @return QString orgName
  */
QString AppSettings::getOrgName()
{
    return settings->value("General/orgName").toString();
}

/**
  * Save Database name
  * @param QString dbName The Database file Name
  */
void AppSettings::setAppDbName(const QString &dbName)
{
    settings->setValue("Database/dbName", dbName);
}

void AppSettings::setExDbName(const QString &dbName)
{
    settings->setValue("Database/exDbName", dbName);
}

/**
  * Save the Mainwindow size and location
  * @param QByteArray byteArray The Window geometry
  */
void AppSettings::setGeometry(const QByteArray &byteArray)
{
    settings->setValue("MainWindow/geometry", byteArray);
}

/**
  * Save the Organisation name
  * @param QString The Organisation name
  */
void AppSettings::setOrgName(const QString &orgName)
{
    settings->setValue("General/companyName", orgName);
}

bool AppSettings::hasDbaseSettings()
{
    if(settings->contains("Database/dbName"))
        return true;
    return false;
}

void AppSettings::write()
{
    this->settings->sync();
}
