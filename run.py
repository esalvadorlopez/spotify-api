from main import main
from send import send
from clean import clean

if __name__ == '__main__':
    main()
    send(clean())
    print('🎉 INFORMACIÓN ENVIADA!')