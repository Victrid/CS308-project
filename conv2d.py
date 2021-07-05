import numpy as np
import tvm
from tvm.topi.nn import conv2d_nchw


def schedule(output):
    s = tvm.te.create_schedule(output.op)
    if output.op.reduce_axis[0].dom.extent > output.op.axis[3].dom.extent:
        s[output].reorder(output.op.axis[0], output.op.axis[1], output.op.reduce_axis[0], output.op.axis[2],
                          output.op.axis[3])
    s[output].parallel(output.op.axis[1])
    s[output].vectorize(output.op.axis[3])
    s[output].unroll(output.op.reduce_axis[2])
    s[output].unroll(output.op.reduce_axis[1])
    return s


def test_topi_conv2d(n, ic, ih, iw, oc, kh, kw):
    # 声明输入输出的大小
    dtype = 'float32'
    # 声明卷积的一些参数
    stride_h, stride_w = (1, 1)
    pad_h, pad_w = (1, 1)
    dilation_h, dilation_w = (1, 1)
    oh = (ih + 2 * pad_h - kh) // stride_h + 1
    ow = (iw + 2 * pad_w - kw) // stride_w + 1
    # 声明占位符
    A = tvm.te.placeholder(shape=(n, ic, ih, iw), dtype=dtype, name='A')
    B = tvm.te.placeholder(shape=(oc, ic, kh, kw), dtype=dtype, name='B')

    # 调用conv2d_nchw来进行conv2d的计算。
    output = conv2d_nchw(Input=A, Filter=B, stride=(stride_h, stride_w), padding=(pad_h, pad_w),
                         dilation=(dilation_h, dilation_w))

    time_original, code_original = run_test(A, B, dtype, ic, ih, iw, kh, kw, n, oc, oh, output, ow,
                                            tvm.te.create_schedule(output.op))
    time_new, code_new = run_test(A, B, dtype, ic, ih, iw, kh, kw, n, oc, oh, output, ow, schedule(output))
    return time_original, time_new, (time_original - time_new) / time_original, str(code_original), str(code_new)


def run_test(A, B, dtype, ic, ih, iw, kh, kw, n, oc, oh, output, ow, s):
    # 编译生成可执行的模块
    func_cpu = tvm.build(s, [A, B, output], target="llvm")

    # 生成数据
    a_np = np.random.uniform(-1, 1, size=(n, ic, ih, iw)).astype(dtype)
    b_np = np.random.uniform(-1, 1, size=(oc, ic, kh, kw)).astype(dtype)
    # 指定底层的运行的硬件
    ctx = tvm.runtime.device("llvm", 0)
    d_cpu = tvm.nd.array(np.zeros((n, oc, oh, ow), dtype=dtype), ctx)
    # 进行转换
    a = tvm.nd.array(a_np, ctx)
    b = tvm.nd.array(b_np, ctx)
    # 执行代码
    func_cpu(a, b, d_cpu)
    # 测试时间
    evaluator = func_cpu.time_evaluator(func_cpu.entry_name, ctx, number=5)
    return evaluator(a, b, d_cpu).mean * 1e3, tvm.lower(s, [A, B, output], simple_mode=True)


def test_suite(test: list[int], identifier: int):
    print("Running test {}".format(identifier))
    time_original, time_new, optimization, code_old, code_new = test_topi_conv2d(*test)
    print('=> Test {} result: original: {:.4f} ms, '
          'optimized: {:.4f} ms, '
          'optimization: {:.2f}%'.format(identifier,
                                         time_original,
                                         time_new,
                                         optimization * 100))
    with open("test{}.old.ir".format(identifier), "w+") as f:
        f.write(code_old)
    print(" -> Original code written to test{}.old.ir".format(identifier))
    with open("test{}.opt.ir".format(identifier), "w+") as f:
        f.write(code_new)
    print(" -> Optimized code written to test{}.opt.ir".format(identifier))


def main():
    test_suite([1, 3, 32, 32, 32, 3, 3], 1)
    test_suite([100, 512, 32, 32, 1024, 3, 3], 2)

    # for 1 iteration of test 2
    # test_suite([1, 512, 32, 32, 1024, 3, 3], 3)


if __name__ == '__main__':
    main()
