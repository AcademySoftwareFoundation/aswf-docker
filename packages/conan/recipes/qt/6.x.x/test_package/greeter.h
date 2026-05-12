/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/9a66422e07df06d2c502501de6e00b8b1213b563/recipes/qt/6.x.x/test_package/greeter.h
*/

#include <QDebug>
#include <QObject>
#include <QString>

class Greeter : public QObject
{
    Q_OBJECT
public:
    Greeter(const QString& name, QObject *parent = 0) 
        : QObject(parent)
        , mName(name) {}

public slots:
    void run()
    {
        qDebug() << QString("Hello %1!").arg(mName);

        emit finished();
    }

signals:
    void finished();
    
private:
    const QString& mName;
};
