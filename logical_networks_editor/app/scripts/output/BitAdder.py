# BitAdder.py 

import re


def format(facts, values):
    a_bits = {}
    b_bits = {}
    out_bits = {}
    carry_in = None
    carry_out = None

    for node_id, value in values.items():
        a_match = re.match(r"A_bit_(\d+)", node_id)
        b_match = re.match(r"B_bit_(\d+)", node_id)
        out_match = re.match(r"Out_bit_(\d+)", node_id)

        if a_match:
            a_bits[int(a_match.group(1))] = int(value)
        elif b_match:
            b_bits[int(b_match.group(1))] = int(value)
        elif out_match:
            out_bits[int(out_match.group(1))] = int(value)
        elif node_id == "INPUT_Carry":
            carry_in = int(value)
        elif node_id == "Out_bit_carry":
            carry_out = int(value)

    def bits_to_binary_str(bits_dict):
        if not bits_dict:
            return None
        n = max(bits_dict.keys()) + 1
        return "".join(str(bits_dict.get(i, 0)) for i in reversed(range(n)))

    def bits_to_int(bits_dict):
        if not bits_dict:
            return None
        return sum(bit << i for i, bit in bits_dict.items())

    A = bits_to_int(a_bits)
    B = bits_to_int(b_bits)
    Out = bits_to_int(out_bits)

    A_bin = bits_to_binary_str(a_bits)
    B_bin = bits_to_binary_str(b_bits)
    Out_bin = bits_to_binary_str(out_bits)

    full_out = None
    full_out_bin = None
    if Out is not None and carry_out is not None and out_bits:
        full_out = Out + (carry_out << len(out_bits))
        full_out_bin = str(carry_out) + Out_bin

    output = ""
    output += "=" * 40 + "\n"
    output += "           ADDER RESULT\n"
    output += "=" * 40 + "\n\n"
    
    if A is not None and B is not None and Out is not None:
        output += f"  {A} + {B} = {full_out if full_out is not None else Out}\n"
        output += f"  {A_bin} + {B_bin} = {full_out_bin if full_out_bin is not None else Out_bin}\n\n"

        if carry_in is not None:
            output += f"(carry in: {carry_in})\n\n"

        expected = A + B + (carry_in or 0)
        actual = full_out if full_out is not None else Out
        status = "! Correct" if expected == actual else "✗ Mismatch"
        output += f"Expected: {expected}    Actual: {actual}    {status}\n"
    else:
        output += "  Incomplete data - missing A, B, or Out bits.\n"

    output += "\n"
    return output
