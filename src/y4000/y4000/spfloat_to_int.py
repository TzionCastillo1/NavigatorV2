def float_to_decimal(float):
    float.reverse()
    sign=1
    if float[0] & 0x80 ==0:
        sign=0
    exponent = ((float[0]<<1)|(float[1]&0x80)>>7)-127;
    mantissa = ((float[1]&0x7f)<<16) | (float[2]<<8)| float[3]

    decimal = pow(-1,sign)*(1.0 + mantissa/pow(2,23))*pow(2,exponent)
    return float(decimal)
