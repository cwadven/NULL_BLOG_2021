# TECH BLOG

## Purpose Of Project

[edit . 2021-10-19]

- Django 지식 고도화 및 TECH 블로그 관리를 위해서 개발 계획

## Project Introduce

[edit . 2021-10-19]

- 내가 공부한 지식 및 꿀팁을 보관해 놓을 창고 역할을 하기 위한 목적
- 지속적으로 습득한 지식을 이용해 보다 나은 모습으로 가꾸기 위한 목적

## Service Address

[edit . 2021-10-19]

https://nulls.co.kr

## Project Duration

[edit . 2021-10-19]

2021-03-16 ~ 2021-03-21 : 첫 배포 완성

2021-03-21 ~ : 유지보수

## Technologies Used

[edit . 2021-10-19]

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

## Deploy

[edit . 2021-10-19]

![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) 

## CI/CD

[edit . 2021-12-18]

![GitHub Actions](https://img.shields.io/badge/githubactions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Developer Information

[edit . 2021-10-19]

#### Developer

##### 👨‍🦱 이창우 (Lee Chang Woo)

- Github : https://github.com/cwadven

## Project Structure

[edit . 2021-10-19]

```
Project Root
├── 📂 config
│    ├── 📜 settings.py
│    ├── 🔒 PRIVATE_SETTING.py
│    ├── 📜 asgi.py
│    ├── 📜 urls.py
│    └── 📜 wsgi.py
│
├── 📂 App Name
│    ├── 📂 migrations                                                      
│    ├── 📜 admin.py                                
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    ├── 📜 tests.py
│    ├── 📜 urls.py
│    ├── 📜 views.py
│    └── 📜 modles.py                                     
│
├── 📂 App Name
│    ├── 📂 migrations                                     
│    ├── 📜 admin.py                                  
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    ├── 📜 tests.py
│    ├── 📜 urls.py
│    ├── 📜 views.py
│    └── 📜 modles.py  
│  
├── 📂 App Name
│    ├── 📂 migrations                                     
│    ├── 📜 admin.py                                  
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    └ .....
│
├── 📂 temp_static
│    ├── 🖼 XXXXX.png                                     
│    ├── 🖼 XXXXX.png                                  
│    ├── 🖼 XXXXX.png
│    ├── 🖼 XXXXX.png
│    └ .....
│
├── 📂 templates
│    └── base.html    
│
├── 🗑 .gitignore                                        # gitignore
├── 🗑 requirements.txt                                  # requirements.txt
└── 📋 README.md                                        # Readme
```

## Database Structure

[edit . 2021-10-19]

생성할 때, Django 의 배경지식이 많이 없어서 Model 에서 정의하는 테이블, 속성 명칭을 잘 못짠 것 같다.

추후 다른 프로젝트를 할 경우는 이런 방식으로 짜면 안될 것 같다.

( id_id 가... 뭐냐.. 쩝... 진짜... 초보적인 실수... 회고 해보면 정말... )

![img.png](img.png)