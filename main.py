import os
import pickle

from get_paired import GetPaired
from symester import Symester


def add_new_symester(get_paired):
    symester = Symester()

    symester_name = str(input("새 학기명을 입력하십시오: "))
    symester.set_name(symester_name)

    str_members = str(input("동아리원들의 이름을 스페이스로 구분하여 입력하십시오: "))
    symester_members = str_members.split()
    symester.set_members(symester_members)

    get_paired.add_symester(symester)


def main():
    print("GetPaired - version 0.0.1")

    if os.path.exists('data.pkl'):
        delete_data = str(input("기존 데이터를 삭제하시겠습니까? (y/n) : "))
        if delete_data.lower() == 'y':
            os.remove('data.pkl')

    if not os.path.exists("data.pkl"):
        with open('data.pkl', 'wb') as f:
            get_paired = GetPaired()
            pickle.dump(get_paired, f)

    with open('data.pkl', 'rb') as f:
        get_paired = pickle.load(f)

    new_symester = str(input("새로운 학기를 시작하시겠습니까? (y/n) : "))
    if new_symester.lower() == 'y':
        add_new_symester(get_paired)
    else:
        if not get_paired.is_symester_exists():
            print("학기 정보가 존재하지 않습니다. 새로운 학기를 생성해야 합니다.")
            add_new_symester(get_paired)

        print("학기를 선택하십시오.")
        get_paired.print_symesters()
        symester_index = int(input("번호(%d~%d) : " % (1, get_paired.num_symesters()))) - 1
        get_paired.set_cur_symester(symester_index)
        get_paired.print_members()

    with open('data.pkl', 'wb') as f:
        pickle.dump(get_paired, f)


if __name__ == '__main__':
    main()