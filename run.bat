@echo off
chcp 936 >nul 2>&1  :: ���ô���ҳΪGBK
title ������Ŀ����

:: ��ȡ�ű�����Ŀ¼����DataBase�ļ��У�
set "BASE_DIR=%~dp0"
:: ȥ��·��ĩβ�ķ�б�ܣ�����У�
if "%BASE_DIR:~-1%"=="\" set "BASE_DIR=%BASE_DIR:~0,-1%"

:: ��������·���������BASE_DIR��
set "CONDA_ENV=%BASE_DIR%\.conda"
set "SERVER_DIR=%BASE_DIR%\server"
set "FRONTEND_DIR=%BASE_DIR%\frontend"

:: ����Ҫ��Ŀ¼�Ƿ����
if not exist "%SERVER_DIR%" (
    echo �����Ҳ���serverĿ¼
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%" (
    echo �����Ҳ���frontendĿ¼
    pause
    exit /b 1
)

:: ������˷���
echo ����������˷���...
start "��˷���" cmd /k "chcp 936 >nul 2>&1 & cd /d "%BASE_DIR%" & conda activate "%CONDA_ENV%" & timeout /t 2 >nul & uvicorn server.main:app --reload"

:: �ȴ�2��ȷ���������
timeout /t 2 >nul

:: ����ǰ�˷���
echo ��������ǰ�˷���...
start "ǰ�˷���" cmd /k "chcp 936 >nul 2>&1 & cd /d "%FRONTEND_DIR%" & npm run dev"

timeout /t 2 >nul

echo ��˺�ǰ�˷���������������ر������������д���
echo ǰ�˿���������ͨ��������: http://localhost:5173
echo ���ʹ�ô���汾�������: http://localhost:4173
echo.
echo ע�⣺DataBase�ļ��е�ǰλ��: %BASE_DIR%
pause