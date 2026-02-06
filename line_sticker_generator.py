#!/usr/bin/env python3
"""สร้างสติกเกอร์ไลน์จากภาพต้นฉบับ + พรอมป์ทด้วย OpenAI Images API."""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path
from typing import Iterable

from openai import OpenAI

LINE_STICKER_SIZE = "1024x1024"


def build_style_prompt(user_prompt: str) -> str:
    return (
        "สร้างภาพสติกเกอร์ตัวละครสไตล์เดียวกับภาพอ้างอิง "
        "โดยรักษาเอกลักษณ์ตัวละครเดิม (สีหน้า, โทนสี, ลายเส้น) "
        "แต่เปลี่ยนท่าทาง/อารมณ์ให้ตรงกับคำสั่งต่อไปนี้: "
        f"{user_prompt}. "
        "ภาพต้องพื้นหลังโปร่งใสหรือพื้นหลังเรียบสะอาด เหมาะกับสติกเกอร์ไลน์ "
        "มีองค์ประกอบชัดเจน ตัวละครเต็มตัว ไม่โดนตัดขอบ"
    )


def generate_stickers(
    client: OpenAI,
    reference_image: Path,
    prompts: Iterable[str],
    out_dir: Path,
    model: str,
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    output_files: list[Path] = []
    for i, prompt in enumerate(prompts, start=1):
        with reference_image.open("rb") as image_file:
            result = client.images.edit(
                model=model,
                image=image_file,
                size=LINE_STICKER_SIZE,
                prompt=build_style_prompt(prompt),
            )

        image_b64 = result.data[0].b64_json
        if not image_b64:
            raise RuntimeError("API ไม่ได้ส่งข้อมูลรูปภาพกลับมา")

        output_path = out_dir / f"sticker_{i:02d}.png"
        output_path.write_bytes(base64.b64decode(image_b64))
        output_files.append(output_path)

    return output_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="สร้างสติกเกอร์ไลน์หลายรูปจากภาพอ้างอิง 1 รูป"
    )
    parser.add_argument("--reference", required=True, help="พาธรูปภาพต้นฉบับ")
    parser.add_argument(
        "--prompt",
        action="append",
        required=True,
        help="คำสั่งสำหรับสร้างท่าทาง/อารมณ์ใหม่ (ระบุได้หลายครั้ง)",
    )
    parser.add_argument(
        "--out-dir",
        default="outputs",
        help="โฟลเดอร์ปลายทางสำหรับไฟล์ PNG",
    )
    parser.add_argument(
        "--model",
        default="gpt-image-1",
        help="โมเดลสร้างภาพ (ค่าเริ่มต้น: gpt-image-1)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("กรุณาตั้งค่า OPENAI_API_KEY ก่อนใช้งาน")

    client = OpenAI(api_key=api_key)
    reference = Path(args.reference)

    if not reference.exists():
        raise FileNotFoundError(f"ไม่พบไฟล์รูปอ้างอิง: {reference}")

    generated = generate_stickers(
        client=client,
        reference_image=reference,
        prompts=args.prompt,
        out_dir=Path(args.out_dir),
        model=args.model,
    )

    print("สร้างสติกเกอร์สำเร็จ:")
    for path in generated:
        print(f"- {path}")


if __name__ == "__main__":
    main()
