# **Pharmazon Backend**
![Pharmazon](assets/logo.png)

## Introduction

Pharmazon is an online marketplace for medicines. The user can upload his/her prescription and with the use of OCR we automatically add the users medicines into his/her cart.

Pharmazon is a smart platform and can suggest alternative medicines or substitutes for the medicines present in the users cart. 

This was made during Hack In The North 4.0 and won the **Best Hack in the Walmart Labs problem statement**

## Technologies

The Backend is made using Flask and MongoDB as the database. We have created an API for the medicine data which we get through scraping [MediPlusSmart](https://www.medplusmart.com/). The OCR is done using Google's Cloud Vision API. Python's Pillow module is used for image manipulation. 

## Frontend

The code for the frontend is present at [Pharmazon](https://github.com/zerefwayne/pharmazon/). The frontend was made by [Aayush Joglekar](https://github.com/zerefwayne) & [Tanmay Mittal](https://github.com/strikertanmay) using Angular.