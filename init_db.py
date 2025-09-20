#!/usr/bin/env python3
"""
SUMA LMS数据库初始化脚本
运行此脚本创建数据库并填充示例数据
"""

import sys
import os

# 将应用目录添加到Python路径
sys.path.append(os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.utils import create_sample_data

def init_database():
    """使用表和示例数据初始化数据库"""
    print("正在初始化SUMA LMS数据库...")
    
    # 创建所有表
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建完成")
    
    # 创建示例数据
    print("正在创建示例数据...")
    db = SessionLocal()
    try:
        create_sample_data(db)
        print("✓ 示例数据创建完成")
    except Exception as e:
        print(f"✗ 创建示例数据时出错: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n🎉 数据库初始化完成！")
    print("\n已创建的示例账户:")
    print("  管理员: admin / admin123")
    print("  教师: teacher / teacher123")
    print("  学生: student1, student2 / student123")
    print("\n现在可以使用以下命令启动API服务器: python -m app.main")

if __name__ == "__main__":
    init_database()
