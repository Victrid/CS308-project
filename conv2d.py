import tvm
import numpy as np
from tvm import autotvm
import logging
from numbers import Integral
from tvm.topi.nn import get_pad_tuple
from tvm.topi.nn import conv2d_nchw
              
# 这个函数是需要大家自己补充的，是需要调用各种schedule的原语进行优化的
# def schedule(output):

        
#ic表示input channel，oc表示output channel      
def test_topi_conv2d():
    # 声明输入输出的大小
    n, ic, ih, iw = 100, 512, 32, 32
    oc, kh, kw = 1024, 3, 3
    dtype = 'float32'
    # 声明卷积的一些参数
    stride_h, stride_w = (1, 1)
    pad_h, pad_w = (1, 1)
    dilation_h, dilation_w = (1, 1)
    oh = (ih + 2 *pad_h - kh) // stride_h + 1
    ow = (iw + 2 * pad_w - kw) // stride_w + 1
    # 声明占位符
    A = tvm.te.placeholder(shape=(n, ic, ih, iw), dtype=dtype, name='A')
    B = tvm.te.placeholder(shape=(oc, ic, kh, kw), dtype=dtype, name='B')
    
    # 调用conv2d_nchw来进行conv2d的计算。
    output = conv2d_nchw(Input = A, Filter = B, stride = (stride_h, stride_w), padding = (pad_h, pad_w), dilation = (dilation_h, dilation_w))
    
    # 这一句是调用tvm默认的schedule函数，表示不加任何优化的schedule
    s = tvm.te.create_schedule(output.op)
    
    # 这里需要大家调用tvm有的原语进行loop循环的优化，大家自己去补充
    # s = schedule(output)

    # 编译生成可执行的模块
    func_cpu = tvm.build(s, [A, B, output], target="llvm")
    # 这个打印进行schedule优化后中间的ir
    print(tvm.lower(s, [A, B, output], simple_mode=True))

    # 生成数据
    a_np = np.random.uniform(-1, 1, size=(n, ic, ih, iw)).astype(dtype)
    b_np = np.random.uniform(-1, 1, size=(oc, ic, kh, kw)).astype(dtype)

    # 指定底层的运行的硬件
    ctx = tvm.runtime.device("llvm",0)
    d_cpu = tvm.nd.array(np.zeros((n, oc, oh, ow), dtype=dtype), ctx)

    # 进行转换
    a = tvm.nd.array(a_np, ctx)
    b = tvm.nd.array(b_np, ctx)
    # 执行代码
    func_cpu(a,  b,  d_cpu)
    # 测试时间
    evaluator = func_cpu.time_evaluator(func_cpu.entry_name, ctx, number=5)
    # 打印时间
    print('Conv: %f ms' % (evaluator(a,b,  d_cpu).mean * 1e3))  
   
def main():
    test_topi_conv2d()
    
if __name__ == '__main__':
    main()



   


