#!/usr/bin/env python

# imports go here

def main():
   # code goes here
    print("main")


if __name__ == '__main__':
    try:
        main()
        print('Program finished')
    except Exception as e:
        print('Error : {}'.format(e))