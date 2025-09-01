import struct
import os
# PE 파일 생성 함수
def create_dummy_pe(filename):
    """
    지정된 PE 파일 구조를 가진 더미 파일을 생성합니다.
    """
    
    # PE 헤더 상수
    IMAGE_DOS_SIGNATURE = b'MZ'
    IMAGE_NT_SIGNATURE = b'PE\0\0'
    
    # 기본 PE 파일 값
    dos_header_size = 0x40
    nt_header_offset = 0x80
    file_alignment = 0x200
    section_alignment = 0x1000
    section_raw_size = 0x200
    
    total_size = nt_header_offset + 248 + (3 * 40) + (3 * section_raw_size)
    print(f"생성될 파일의 예상 크기: {total_size} 바이트 (5KB 미만)")
    
    with open(filename, 'wb') as f:
        # 1. DOS 헤더
        f.write(struct.pack('<H', 0x4d5a))  # e_magic (MZ)
        f.write(struct.pack('<H', 0x0090))
        f.write(struct.pack('<H', 0x0003))
        f.write(struct.pack('<H', 0x0000))
        f.write(struct.pack('<H', 0x0004))
        f.write(struct.pack('<H', 0x0000))
        f.write(struct.pack('<H', 0x0000))
        f.write(struct.pack('<H', 0x0000))
        f.write(struct.pack('<H', 0x00b8))
        f.write(struct.pack('<H', 0x0000))
        f.write(struct.pack('<H', 0x0000))
        f.write(struct.pack('<H', 0x0000))
        f.write(struct.pack('<H', 0x0040))
        f.write(struct.pack('<H', 0x0000))
        f.write(b'\0' * 8)
        f.write(struct.pack('<H', 0x0000))
        f.write(struct.pack('<H', 0x0000))
        f.write(b'\0' * 20)
        f.write(struct.pack('<L', nt_header_offset))
        
        # 2. DOS 스텁
        f.write(b'\0' * (nt_header_offset - dos_header_size))
        
        # 3. NT 헤더
        f.write(IMAGE_NT_SIGNATURE)
        
        # 파일 헤더
        num_sections = 3
        f.write(struct.pack('<H', 0x014c))
        f.write(struct.pack('<H', num_sections))
        f.write(struct.pack('<L', 0x00000000))
        f.write(struct.pack('<L', 0x00000000))
        f.write(struct.pack('<L', 0x00000000))
        f.write(struct.pack('<H', 0x00e0))
        f.write(struct.pack('<H', 0x010f))
        
        # 옵셔널 헤더
        f.write(struct.pack('<H', 0x010b))
        f.write(b'\0' * 2)
        f.write(struct.pack('<L', 0x00000000))
        f.write(struct.pack('<L', 0x00000000))
        f.write(struct.pack('<L', 0x00000000))
        f.write(struct.pack('<L', 0x00000000))
        f.write(struct.pack('<L', 0x00001000))
        f.write(struct.pack('<L', 0x00000000))
        f.write(struct.pack('<L', 0x00400000))
        f.write(struct.pack('<L', section_alignment))
        f.write(struct.pack('<L', file_alignment))
        f.write(b'\0' * 8)
        f.write(b'\0' * 4)
        f.write(b'\0' * 4)
        f.write(struct.pack('<L', nt_header_offset + 248 + 120))
        f.write(b'\0' * 4)
        f.write(struct.pack('<H', 0x0002))
        f.write(b'\0' * 2)
        f.write(b'\0' * 8)
        f.write(b'\0' * 8)
        f.write(b'\0' * 4)
        f.write(struct.pack('<L', 0x10))
        f.write(b'\0' * 128)
        
        # 4. 섹션 헤더
        f.write(b'.text\0\0\0')
        f.write(struct.pack('<L', 0x00000200))
        f.write(struct.pack('<L', 0x00001000))
        f.write(struct.pack('<L', section_raw_size))
        f.write(struct.pack('<L', nt_header_offset + 248 + 120))
        f.write(b'\0' * 8)
        f.write(struct.pack('<L', 0x60000020))
        
        f.write(b'.data\0\0\0')
        f.write(struct.pack('<L', 0x00000200))
        f.write(struct.pack('<L', 0x00002000))
        f.write(struct.pack('<L', section_raw_size))
        f.write(struct.pack('<L', f.tell()))
        f.write(b'\0' * 8)
        f.write(struct.pack('<L', 0xC0000040))
        
        f.write(b'.rsrc\0\0\0')
        f.write(struct.pack('<L', 0x00000200))
        f.write(struct.pack('<L', 0x00003000))
        f.write(struct.pack('<L', section_raw_size))
        f.write(struct.pack('<L', f.tell()))
        f.write(b'\0' * 8)
        f.write(struct.pack('<L', 0x40000040))
        
        # 5. 섹션 데이터
        current_offset = f.tell()
        padding_needed = (nt_header_offset + 248 + 120) - current_offset
        if padding_needed > 0:
            f.write(b'\0' * padding_needed)

        f.write(b'\0' * section_raw_size)
        f.write(b'\0' * section_raw_size)
        f.write(b'\0' * section_raw_size)

    print(f"\n✅ '{filename}' 파일이 성공적으로 생성되었습니다.")
    print(f"파일 크기: {os.path.getsize(filename)} 바이트")

create_dummy_pe("test_dummy_pe.exe")