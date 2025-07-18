# -*- coding: utf-8 -*-
# @Project: auto_tester
# @File: test_select_statistics.py
# @Author: Wakka
# @Date: 2025/07/02 16:42
# @Desc: 查询年度，月税费

import pytest

from common.prepare_api import AllApi


class TestSupplierMaterial:
    @pytest.mark.parametrize("api_name", ["SelectMaterialCategory"])
    def test_select_material_category_valid(
        self,
        shared_data: dict,
        api_name: str,
        all_api: AllApi,
    ):
        """
        测试查询SCM材料分类接口
        """
        res = all_api.send_request(api_name)
        expect = all_api.get_expect(api_name)

        assert res["code"] == expect["code"], (
            f"code: {res['code']}, 预期结果: {expect['code']}"
        )
        assert res["msg"] == expect["msg"], (
            f"msg: {res['msg']}, 预期结果: {expect['msg']}"
        )
        if res["code"] == 200:
            material_id = res["data"][-1]["id"]
            assert material_id, f"获取的material_id为空: {material_id}"
            # 存入共享数据
            shared_data["id"] = material_id
            # print("共享数据", shared_data)

    @pytest.mark.parametrize("api_params", ["AddMaterialCategory"], indirect=True)
    def test_add_material_category_valid(self, api_params: dict, all_api: AllApi):
        """
        测试修改SCM材料分类接口
        """
        # 打印合并后的请求参数（供调试）
        # print("新增参数：", api_params)
        api_name = api_params["api_name"]
        print(api_name)

        res = all_api.send_request(api_name)
        expect = all_api.get_expect(api_name)

        # 断言
        assert res["code"] == expect["code"], (
            f"code: {res['code']}, 预期结果: {expect['code']}"
        )
        assert res["msg"] == expect["msg"], (
            f"msg: {res['msg']}, 预期结果: {expect['msg']}"
        )


def main():
    test = TestSupplierMaterial()
    test.test_select_material_category_valid("SelectMaterialCategory")
    # pass


if __name__ == "__main__":
    main()
