/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/qt/6.x.x/test_package/test_package.cpp
*/

#include <QCoreApplication>
#include <QObject>
#include <QString>
#include <QTimer>
#include <QFile>

#include <QNetworkAccessManager>
#include <QSqlDatabase>
#include <qtconcurrentfilter.h>
#include <QDomText>

#include "greeter.h"

int main(int argc, char *argv[]){
    QCoreApplication app(argc, argv);
    QCoreApplication::setApplicationName("Application Example");
    QCoreApplication::setApplicationVersion("1.0.0");

    QString name = argc > 0 ? argv[1] : "";
    if (name.isEmpty()) {
        name = "World";
    }

    Greeter* greeter = new Greeter(name, &app);
    QObject::connect(greeter, SIGNAL(finished()), &app, SLOT(quit()));
    QTimer::singleShot(0, greeter, SLOT(run()));

    QFile f(":/resource.txt");
    if(!f.open(QIODevice::ReadOnly))
        qFatal("Could not open resource file");
    qDebug() << "Resource content:" << f.readAll();
    f.close();

    QNetworkAccessManager networkTester;

    QSqlDatabase sqlTester;

    QVector<int> v;
    v << 1 << 2 << 3 << 4;
    QtConcurrent::blockingFilter(v, [](int i)
    {
        return i % 2;
    });

    QDomText xmlTester;

    return app.exec();
}
