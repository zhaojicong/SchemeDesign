__author__ = 'Jack'
from ListNode import *

class Solution(object):
    @staticmethod
    def isIsomorphic(s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        if len(s)==len(t):
            return True
        else:
            return False

    @staticmethod
    def titleToNumber(s):
        """
        :type s: str
        :rtype: int
        """
        dt = {}
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(1,27):
            dt.__setitem__(alphabet[i-1],i)
        sum = 0
        for char in s:
            sum = sum*26 + dt.get(char)
        return sum

    @staticmethod
    def sortArray1(str):
        for i in range(0,len(str)):
            for j in range(i+1,len(str)):
                if str[i]>str[j]:
                    temp = str[i]
                    str[i] = str[j]
                    str[j] = temp
        return str

    @staticmethod
    def sortArray2(str):
        for i in range(1,len(str)):
            for j in range(0,i):
                if str[i]<str[j]:
                    temp = str[i]
                    for k in range(i,j,-1):
                        str[k] = str[k-1]
                    str[j] = temp
        return str

    @staticmethod
    def trailingZeroes(n):
        """
        :type n: int
        :rtype: int
        """
        times = 0
        for i in range(1, n+1, 1):
            j = i
            while j%5 == 0:
                times += 1
                j = j/5
        return times

    @staticmethod
    def convertToTitle( n):
        """
        :type n: int
        :rtype: str
        """
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        title = ''
        if n>26:
            while n/26 != 0 and n != 26:
                temp = n%26
                if temp == 0:
                    title = alphabet[25]+title
                    temp = 26
                else:
                    title = alphabet[temp-1]+title
                n = (n-temp)/26
        temp = n%26
        if temp == 0:
            title = alphabet[25]+title
        else:
            title = alphabet[temp-1]+title
        return title

    @staticmethod
    def getIntersectionNode(headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """
        if headA == None or headB == None:
            return None
        else:
            temp = ListNode(0)
            temp.next = headB
            while headA.next != None:
                while headB.next!=None:
                    if headB.next.val==headA.next.val:
                        return headA.next
                    headB = headB.next
                headA = headA.next
                headB = temp.next
            return None

    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        product = []
        for i in range(0,len(nums)):
            for j in range(i,len(nums)):
                product.append(nums[i]*nums[j])
        product.sort()
        return product[len(product)-1]

# headA = None
# # headA.next = ListNode(4)
# # headA.next.next = ListNode(5)
# # headA.next.next.next = ListNode(6)
# # headA.next.next.next.next = ListNode(7)
# headB = None
# # headB.next = ListNode(1)
# # headB.next.next = ListNode(2)
# # headB.next.next.next = ListNode(5)
# # headB.next.next.next.next = ListNode(6)
# # headB.next.next.next.next.next = ListNode(7)
#
# head = Solution.getIntersectionNode(headA,headB)
# print head.val
# solve = Solution()
# x = [2, 6, 5, 8, 3, 4, 9, 1, 7]
# x.sort()
# print x
# print Solution.titleToNumber("ZA")
# a = timeit.timeit()
# print Solution.sortArray1(x)
# b = timeit.timeit()
# print a-b
# c = timeit.timeit()
# print Solution.sortArray2(x)
# d = timeit.timeit()
# # print c-d
# print Solution.convertToTitle(27)
# c = 'a'+'b'
# print c[1]

