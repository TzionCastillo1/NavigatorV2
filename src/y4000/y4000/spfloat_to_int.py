def float_to_decimal(fp):
    fp.reverse()
    sign=1
    if fp[0] & 0x80 ==0:
        sign=0
    exponent = ((fp[0]<<1)|(fp[1]&0x80)>>7)-127;
    mantissa = ((fp[1]&0x7f)<<16) | (fp[2]<<8)| fp[3]

    decimal = pow(-1,sign)*(1.0 + mantissa/pow(2,23))*pow(2,exponent)
    return decimal
