"""설치한 라이브러리 세 개가 잘 들어갔는지 확인한다.
실행: python check_libs.py
세 줄에 버전 숫자가 나오면 성공이다. ModuleNotFoundError가 나오면
그 이름의 라이브러리를 pip install 로 다시 설치한다.
"""
import pygame
import numpy
import sklearn

print("pygame", pygame.version.ver)
print("numpy", numpy.__version__)
print("scikit-learn", sklearn.__version__)
