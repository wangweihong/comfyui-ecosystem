import argparse
import base64
import hashlib
import os
import random
import string

import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def generate_iv():
    """生成随机的初始化向量"""
    return os.urandom(AES.block_size)
def derive_key(password, salt=None):
    """使用PBKDF2算法从密码派生密钥"""
    if salt is None:
        salt = os.urandom(16)
    
    # 使用PBKDF2-HMAC-SHA256派生密钥
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, 32)
    return key, salt
def apply_text_confusion(text, key, mode='basic'):
    """
    应用文字混淆
    :param text: 原始文本
    :param key: 混淆密钥
    :param mode: 混淆模式 ('basic', 'advanced', 'aes')
    :return: 混淆后的文本和附加数据
    """
    if mode == 'basic':
        # 基本混淆：字符替换和位置置换
        return basic_text_confusion(text, key)
    elif mode == 'advanced':
        # 高级混淆：多级变换
        return advanced_text_confusion(text, key)
    elif mode == 'aes':
        # AES加密
        return aes_encrypt(text, key)
    else:
        raise ValueError(f"未知的混淆模式: {mode}")
def basic_text_confusion(text, key):
    """基本文字混淆：字符替换和位置置换"""
    # 字符替换映射表
    mapping = list(string.ascii_letters + string.digits + string.punctuation + " ")
    shuffled_mapping = mapping.copy()
    random.seed(key)
    random.shuffle(shuffled_mapping)
    
    # 创建替换字典
    char_map = dict(zip(mapping, shuffled_mapping))
    
    # 应用字符替换
    confused_text = ''.join(char_map.get(c, c) for c in text)
    
    # 位置置换
    char_list = list(confused_text)
    np.random.seed(key)
    permutation = np.random.permutation(len(char_list))
    shuffled_chars = np.array(char_list)[permutation]
    
    return ''.join(shuffled_chars), permutation
def advanced_text_confusion(text, key):
    """高级文字混淆：多级变换"""
    # 第一步：Base64编码
    encoded = base64.b64encode(text.encode()).decode()
    
    # 第二步：字符替换
    mapping = list(string.ascii_letters + string.digits + string.punctuation)
    shuffled_mapping = mapping.copy()
    random.seed(key)
    random.shuffle(shuffled_mapping)
    char_map = dict(zip(mapping, shuffled_mapping))
    replaced_text = ''.join(char_map.get(c, c) for c in encoded)
    
    # 第三步：位置置换
    char_list = list(replaced_text)
    np.random.seed(key)
    permutation = np.random.permutation(len(char_list))
    shuffled_chars = np.array(char_list)[permutation]
    
    return ''.join(shuffled_chars), permutation
def restore_text(confused_text, key, permutation=None, mode='basic'):
    """
    还原混淆文本
    :param confused_text: 混淆后的文本
    :param key: 混淆密钥
    :param permutation: 位置置换顺序 (仅用于basic和advanced模式)
    :param mode: 混淆模式
    :return: 还原后的原始文本
    """
    if mode == 'basic':
        return basic_text_restore(confused_text, key, permutation)
    elif mode == 'advanced':
        return advanced_text_restore(confused_text, key, permutation)
    elif mode == 'aes':
        return aes_decrypt(confused_text, key)
    else:
        raise ValueError(f"未知的还原模式: {mode}")
def basic_text_restore(confused_text, key, permutation):
    """还原基本混淆文本"""
    # 还原位置置换
    char_list = list(confused_text)
    np.random.seed(key)
    original_permutation = np.random.permutation(len(char_list))
    
    # 创建逆置换索引
    inverse_permutation = np.argsort(permutation)
    restored_chars = np.array(char_list)[inverse_permutation]
    
    # 创建字符替换映射表
    mapping = list(string.ascii_letters + string.digits + string.punctuation + " ")
    shuffled_mapping = mapping.copy()
    random.seed(key)
    random.shuffle(shuffled_mapping)
    
    # 创建反向映射字典
    reverse_map = dict(zip(shuffled_mapping, mapping))
    
    # 应用反向字符替换
    restored_text = ''.join(reverse_map.get(c, c) for c in restored_chars)
    
    return restored_text
def advanced_text_restore(confused_text, key, permutation):
    """还原高级混淆文本"""
    # 还原位置置换
    char_list = list(confused_text)
    inverse_permutation = np.argsort(permutation)
    restored_chars = np.array(char_list)[inverse_permutation]
    restored_text = ''.join(restored_chars)
    
    # 还原字符替换
    mapping = list(string.ascii_letters + string.digits + string.punctuation)
    shuffled_mapping = mapping.copy()
    random.seed(key)
    random.shuffle(shuffled_mapping)
    reverse_map = dict(zip(shuffled_mapping, mapping))
    
    replaced_text = ''.join(reverse_map.get(c, c) for c in restored_text)
    
    # Base64解码
    try:
        decoded_bytes = base64.b64decode(replaced_text)
        return decoded_bytes.decode()
    except:
        return "解码错误 - 请检查密钥是否正确"
def aes_encrypt(text, password):
    """使用AES加密文本"""
    # 派生密钥和盐
    key, salt = derive_key(password)
    
    # 生成初始化向量
    iv = generate_iv()
    
    # 创建AES加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 加密文本
    padded_text = pad(text.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    
    # 组合结果：盐 + IV + 密文
    combined = salt + iv + ciphertext
    return base64.b64encode(combined).decode()
def aes_decrypt(encrypted_text, password):
    """使用AES解密文本"""
    try:
        # 解码Base64
        combined = base64.b64decode(encrypted_text)
        
        # 提取盐、IV和密文
        salt = combined[:16]
        iv = combined[16:16 + AES.block_size]
        ciphertext = combined[16 + AES.block_size:]
        
        # 派生密钥
        key, _ = derive_key(password, salt)
        
        # 创建AES解密器
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # 解密
        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted = unpad(decrypted_padded, AES.block_size)
        
        return decrypted.decode()
    except Exception as e:
        return f"解密错误: {str(e)}"
def process_file(input_path, key, output_dir, prefix, mode='confuse', text_mode='basic'):
    """
    处理单个文件
    :param input_path: 输入文件路径
    :param key: 密钥
    :param output_dir: 输出目录
    :param prefix: 输出文件前缀
    :param mode: 处理模式 ('confuse' 或 'restore')
    :param text_mode: 文本混淆模式 ('basic', 'advanced', 'aes')
    """
    try:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取文件名和扩展名
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        
        # 构建输出路径
        output_filename = f"{prefix}{name}{ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        # 读取文件内容
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if mode == 'confuse':
            # 混淆处理
            if text_mode == 'aes':
                # AES模式不需要额外的置换数据
                confused_content = apply_text_confusion(content, key, text_mode)
                permutation = None
            else:
                confused_content, permutation = apply_text_confusion(content, key, text_mode)
            
            # 保存混淆后的内容
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(confused_content)
            
            # 如果不是AES模式，保存置换数据
            if text_mode != 'aes':
                permutation_path = os.path.join(output_dir, f"{prefix}{name}_perm.npy")
                np.save(permutation_path, permutation)
            
            print(f"混淆成功: {input_path} -> {output_path}")
            return True
            
        elif mode == 'restore':
            # 还原处理
            if text_mode != 'aes':
                # 查找置换数据文件
                permutation_path = os.path.join(os.path.dirname(input_path), f"{prefix}{name}_perm.npy")
                if not os.path.exists(permutation_path):
                    print(f"找不到置换数据文件: {permutation_path}")
                    return False
                
                permutation = np.load(permutation_path)
            else:
                permutation = None
            
            restored_content = restore_text(content, key, permutation, text_mode)
            
            # 保存还原后的内容
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(restored_content)
            
            print(f"还原成功: {input_path} -> {output_path}")
            return True
    
    except Exception as e:
        print(f"处理失败: {input_path} - {str(e)}")
        return False
def process_directory(input_dir, key, output_dir, prefix, mode='confuse', text_mode='basic', recursive=True):
    """
    处理目录下的所有文本文件
    :param input_dir: 输入目录
    :param key: 密钥
    :param output_dir: 输出目录
    :param prefix: 输出文件前缀
    :param mode: 处理模式 ('confuse' 或 'restore')
    :param text_mode: 文本混淆模式 ('basic', 'advanced', 'aes')
    :param recursive: 是否递归处理子目录
    """
    # 支持的文本文件格式
    supported_formats = ['.txt', '.csv', '.json', '.xml', '.html', '.md']
    
    processed_count = 0
    skipped_count = 0
    
    # 遍历目录
    for root, _, files in os.walk(input_dir):
        # 如果不递归处理子目录，只处理顶层目录
        if not recursive and root != input_dir:
            continue
            
        for file in files:
            # 检查文件扩展名
            if any(file.lower().endswith(ext) for ext in supported_formats):
                file_path = os.path.join(root, file)
                if process_file(file_path, key, output_dir, prefix, mode, text_mode):
                    processed_count += 1
                else:
                    skipped_count += 1
    
    print(f"\n处理完成！共处理 {processed_count} 个文件，跳过 {skipped_count} 个文件")
def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='文字混淆与还原工具')
    parser.add_argument('input', help='输入文件或目录路径')
    parser.add_argument('key', help='混淆密钥 (字符串)')
    parser.add_argument('--mode', choices=['confuse', 'restore'], default='confuse', 
                        help='处理模式: confuse(混淆)或restore(还原)')
    parser.add_argument('--output', default='output', help='输出目录路径 (默认为"output")')
    parser.add_argument('--prefix', default='', help='输出文件前缀 (默认为空)')
    parser.add_argument('--text-mode', choices=['basic', 'advanced', 'aes'], default='basic', 
                        help='文本混淆模式: basic(基本), advanced(高级), aes(AES加密)')
    parser.add_argument('--no-recursive', action='store_true', 
                        help='不递归处理子目录')
    
    args = parser.parse_args()
    
    # 检查输入路径是文件还是目录
    if os.path.isfile(args.input):
        # 处理单个文件
        process_file(
            input_path=args.input,
            key=args.key,
            output_dir=args.output,
            prefix=args.prefix,
            mode=args.mode,
            text_mode=args.text_mode
        )
    elif os.path.isdir(args.input):
        # 处理目录
        process_directory(
            input_dir=args.input,
            key=args.key,
            output_dir=args.output,
            prefix=args.prefix,
            mode=args.mode,
            text_mode=args.text_mode,
            recursive=not args.no_recursive
        )
    else:
        print(f"错误: 路径 '{args.input}' 不存在或不是文件/目录")
if __name__ == "__main__":
    main()