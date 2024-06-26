import streamlit as st
import pandas as pd
import uuid
import json
import datetime
from lark_connector import connect_to_larkbase, get_larkbase_data, get_tenant_access_token, get_list_table, get_list_view, create_a_record, create_records
import unidecode
import json
import requests
from requests.auth import HTTPBasicAuth
import base64
import os



def login():    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ''

    if not st.session_state.logged_in:
        st.write("Vui lòng đăng nhập để tiếp tục")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Đăng nhập", type="primary"):
            if username in st.secrets["login"]["users"] and password == st.secrets["login"]["users"][username]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error("Sai tài khoản mật khẩu")
                st.info("Cấp lại tài khoản mật khẩu -> liên hệ admin.")
    else:
        st.write(f"Xin chào {st.session_state.username}!")
        with st.popover("Xem nội dung cập nhật."):
            st.info("Cập nhật: 10/06/2024.")
            st.write("1. Thêm form giống như form ở larkbase")
            st.write("2. Chỉ hiển thị ra danh sách khách hàng đã 'chốt'")
            st.write("---")
            st.info("Cập nhật: 16/06/2024.")
            st.write("1. Fix bug linh tinh")
            st.write("2. Thêm video hướng dẫn - sắp ra mắt")
            st.write("3. Thêm tính năng login nhiều user - ghi lại user khi gửi dữ liệu.")
            st.write("---")
            st.info("Cập nhật: 19/06/2024.")
            st.write("1. Fix bug: không thể kết nối đến dữ liệu (lỗi hết hạn token)")
            st.write("2. Thêm tính năng login nhiều user - ghi lại user khi gửi dữ liệu. (tk mk cần thì gửi thượng để thượng cài)")
            st.write("---")
        with st.popover("Xem kế hoạch cập nhật."):
            st.write("1. Thêm thanh navibar cho dễ theo dõi tab")
            st.write("2. Update tính năng login tự động check tkmk")
            
        user = st.secrets["user"]
        password = st.secrets["password"]

        lark_app_id = st.secrets["lark_app_id"]
        lark_app_secret = st.secrets["lark_app_secret"]
        lark_app_token = st.secrets["lark_app_token"]

        table_customer_id = st.secrets["table_customer_id"]
        table_order_id = st.secrets["table_order_id"]
        table_orders_id = st.secrets["table_orders_id"]
        table_product_id = st.secrets["table_product_id"]
        st.session_state.tenant_access_token = get_tenant_access_token(lark_app_id, lark_app_secret)
        
        
        # Tiêu đề app
        if 'tenant_access_token' not in st.session_state:
            st.session_state.tenant_access_token = None
            
        # st.session_state.tenant_access_token = get_tenant_access_token(lark_app_id, lark_app_secret)

        if st.session_state.tenant_access_token is None:
            st.session_state.tenant_access_token = get_tenant_access_token(lark_app_id, lark_app_secret)
            tenant_access_token = st.session_state.tenant_access_token
            if tenant_access_token is not None:
                st.write("Đang kết nối đến dữ liệu trong file Larkbase...")
            else:
                st.error("Không thể tạo tenant_access_token. Vui lòng kiểm tra lại App ID và App Secret.")

        def get_larkbase_table_data(table_id, filter=None):
            return get_larkbase_data(st.session_state.tenant_access_token, lark_app_token, table_id, filter = filter,  app_id=lark_app_id, app_secret=lark_app_secret)

        def save_df_to_json(df, file_name):
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(df.to_dict(orient="records"), file, ensure_ascii=False, indent=4)
                
        if st.session_state.tenant_access_token is not None:
            table_ids = [table_customer_id, table_product_id]
            table_names = ["table_customer", "table_product"]
            dfs = {}
            
            for table_id, table_name in zip(table_ids, table_names):
                st.info("Đang lấy dữ liệu từ: "+table_name)
                if table_name == "table_customer":
                    #chỉ lấy ra khách hàng nào đã chốt thôi
                    filter = {
                        "filter": {
                            "conditions": [
                                {
                                    "field_name": "Tình trạng",
                                    "operator": "is",
                                    "value": [
                                        "Chốt"
                                    ]
                                }
                            ],
                            "conjunction": "and"
                        }
                    }
                    
                    data = get_larkbase_table_data(table_id,filter)
                else:
                    data = get_larkbase_table_data(table_id)
                    
                if data is not None:
                    dfs[table_name] = pd.DataFrame(data)
                    # save_df_to_json(dfs[table_name], f"{table_name}.json")  # Lưu DataFrame vào file JSON

                else:
                    st.error(f"Kết nối đến bảng {table_name} thất bại!")
            
            if len(dfs) == len(table_names):
                st.success("Kết nối và lấy dữ liệu từ Larkbase thành công!")
            else:
                st.error("Kết nối và lấy dữ liệu từ Larkbase thất bại!")
        else:
            st.warning("Vui lòng tạo tenant_access_token trước khi kết nối với Larkbase.")

        # Đọc dữ liệu khách hàng từ DataFrame
        customer_data = dfs["table_customer"].to_dict('records')
        product_data = dfs["table_product"].to_dict('records')


        # Tạo danh sách Nguồn khách hàng
        
        customer_source_list = list(set([customer['fields'].get('Nguồn khách hàng', '') for customer in customer_data if customer['fields'].get('Nguồn khách hàng', '')]))



        # Sắp xếp danh sách khách hàng theo ngày tạo (mới nhất lên trên)
        sorted_customer_data = sorted(customer_data, key=lambda x: x['fields'].get('Thời gian tạo', 0), reverse=True)
        # Tạo danh sách khách hàng để hiển thị trong dropdown
        customer_list = [customer['fields'].get('ID khách hàng', {'value': [{'text': ''}]})['value'][0]['text'] for customer in sorted_customer_data]

        # Form nhập thông tin khách hàng
        st.header("Thông tin khách hàng")

        # Tùy chọn thêm mới hoặc chọn khách hàng có sẵn
        customer_option = st.radio("Lựa chọn khách hàng", ("Thêm mới", "Chọn từ danh sách"))

        if customer_option == "Thêm mới":
            # Nhập thông tin khách hàng mới
            customer_name = st.text_input("Tên khách hàng", placeholder= "Nhập tên khách hàng...")
            customer_phone = st.text_input("Số điện thoại", placeholder="Chỉ nhập dạng số ví dụ 0816226086")
            customer_ad_channel = st.selectbox("Nguồn khách hàng", customer_source_list, index=customer_source_list.index("FB Mới"))
            customer_notes = st.text_area("Ghi chú", placeholder="Nhập ghi chú nếu có (ghi chú về khách hàng)")
            is_new = "yes"
            customer_record_id = ""
            st.info("Thông tin khách hàng sẽ được thêm mới khi bạn lưu đơn hàng!")
            
            #bỏ để vào anycross cho nó tự động tạo nhé.
            # # Tạo bản ghi mới cho khách hàng 
            # if st.button("Thêm khách hàng mới"):
            #     if customer_name and customer_phone:
            #         body = {
            #             "fields": {
            #                 "Tên khách hàng": customer_name,
            #                 "Số điện thoại": customer_phone,
            #                 "Nguồn khách hàng": customer_ad_channel,
            #                 "Ghi chú": customer_notes,
            #             }
            #         }
                    
            #         # Gọi hàm create_a_record để tạo bản ghi mới
            #         new_record_id = create_a_record(st.session_state.tenant_access_token, lark_app_token, table_customer_id, body, app_id=lark_app_id, app_secret=lark_app_secret)
                    
            #         if new_record_id:
            #             st.success(f"Đã thêm khách hàng mới với ID: {new_record_id}")
            #         else:
            #             st.error("Không thể thêm khách hàng mới. Vui lòng thử lại.")
            #     else:
            #         st.warning("Vui lòng nhập tên và số điện thoại của khách hàng.")
                    
        else:
            # Chọn khách hàng từ danh sách
            st.info("Dưới đây là danh sách khách hàng đã chốt!")
            selected_customer = st.selectbox("Chọn khách hàng", customer_list)
            is_new = "no"
            
            # Lấy thông tin khách hàng đã chọn
            # selected_customer_data = next(customer for customer in customer_data if customer['fields']['ID khách hàng'][0]['text'] == selected_customer)
            
            selected_customer_data = next(
                (customer for customer in customer_data if customer['fields'].get('ID khách hàng', {'value': [{'text': ''}]})['value'][0]['text'] == selected_customer),
                None
            )        
            
            customer_id_value = selected_customer_data['fields'].get('ID khách hàng', {'value': [{'text': ''}]})['value'][0]['text']
            customer_name = customer_id_value.split(' - ')[0] if ' - ' in customer_id_value else ''
            customer_phone = customer_id_value.split(' - ')[1] if ' - ' in customer_id_value and len(customer_id_value.split(' - ')) > 1 else ''
            customer_email = selected_customer_data['fields'].get('Email', [{'text': ''}])[0]['text']
            customer_ad_channel = selected_customer_data['fields'].get('Nguồn khách hàng', '')
            customer_notes = selected_customer_data['fields'].get('Ghi chú', [{'text': ''}])[0]['text']
            customer_record_id = selected_customer_data.get('record_id', '')
            
            
        # Hiển thị thông tin khách hàng đã chọn hoặc nhập
        st.subheader("Thông tin khách hàng")
        st.write(f"Tên khách hàng: {customer_name}")
        st.write(f"Số điện thoại: {customer_phone}")
        st.write(f"Nguồn khách hàng: {customer_ad_channel}")
        st.write(f"Ghi chú: {customer_notes}")




        def remove_item(index):
            st.session_state.order_items.pop(index)


        # Đọc thông tin sản phẩm từ DataFrame
        product_data = dfs["table_product"].to_dict('records')

        # Khởi tạo session state
        if 'order_items' not in st.session_state:
            st.session_state.order_items = []

        # Chọn sản phẩm và số lượng
        st.header("Thông tin đơn hàng")
        
        

        col1, col2, col3 = st.columns(3)

        with col1:
            hinh_thuc_don_hang_list = ["Vật tư", "Hoàn thiện", "Đơn keo"]
            hinh_thuc_don_hang = st.selectbox("Hình thức đơn hàng", hinh_thuc_don_hang_list, index=hinh_thuc_don_hang_list.index("Vật tư"))

        with col2:
            hinh_thuc_thanh_toan_list = ["Thanh toán trước", "Thanh toán khi nhận hàng"]
            hinh_thuc_thanh_toan = st.selectbox("Hình thức thanh toán", hinh_thuc_thanh_toan_list)

        with col3:
            tinh_trang_chot_list = ["Chưa cọc", "Đã cọc"]
            tinh_trang_chot = st.selectbox("Tình trạng cọc", tinh_trang_chot_list)

        st.write("")
        if st.button("Thêm sản phẩm"):
            st.session_state.order_items.append({
                'product_id': '',
                'product_name': '',
                'quantity': 1,
                'price': 0,
                'unit': '',
                'category': '',
                'type': '',
                'note': '',
                'subtotal': 0
            })
        product_ids = sorted(list(set(product['fields']['Mã vật tư'] for product in product_data if product['fields'].get('Mã vật tư'))))
        order_items_df = pd.DataFrame(st.session_state.order_items)
        for index, order_item in order_items_df.iterrows():
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([0.5, 3, 1, 2, 1, 1, 1, 2, 2])
            
            with col1:
                st.write(f"#{index + 1}")
            
            with col2:
                
                product_id = st.selectbox("Mã vật tư", [''] + product_ids, key=f'product_{index}')
                # product_id = st.selectbox("Mã vật tư", [''] + [product['fields']['Mã vật tư'] for product in product_data], key=f'product_{index}')
                if product_id != '':
                    product = next(product for product in product_data if product['fields']['Mã vật tư'] == product_id)
                    order_items_df.at[index, 'product_id'] = product_id
                else:
                    order_items_df.at[index, 'product_id'] = ''
            
            with col3:
                quantity = st.number_input("SL", min_value=1, value=order_item['quantity'], key=f'quantity_{index}')
                order_items_df.at[index, 'quantity'] = quantity
            
            with col4:
                default_price = product['fields']['Đơn giá'] if product_id != '' else 0
                price = st.number_input("Đơn giá", value=float(default_price), key=f'price_{index}', format="%.0f")
                order_items_df.at[index, 'price'] = price
                
            with col5:
                unit = product['fields']['Đơn vị tính (khi lên đơn)'] if product_id != '' else ''
                st.write(f"ĐVT: {unit}")
                order_items_df.at[index, 'unit'] = unit
            
            with col6:
                category = product['fields']['Nhóm'] if product_id != '' else ''
                st.write(f"Nhóm: {category}")
                order_items_df.at[index, 'category'] = category
            
            with col7:
                product_type = product['fields']['Loại'] if product_id != '' else ''
                st.write(f"Loại: {product_type}")
                order_items_df.at[index, 'type'] = product_type
            
            with col8:
                note = st.text_input("Ghi chú", key=f'note_{index}')
                order_items_df.at[index, 'note'] = note
                
            with col9:
                subtotal = quantity * price
                order_items_df.at[index, 'subtotal'] = subtotal
                st.write(f"Thành tiền: {subtotal:,.0f} VNĐ")

        st.session_state.order_items = order_items_df.to_dict('records')

        st.info("Chỗ tính tổng thành tiền chưa hoàn thiện, do có sản phẩm tính theo m2 *1,03 chỗ này cần phải thảo luận lại!!!")
        st.info("Nhưng yên tâm, khi dữ liệu lưu ở table 4. Quản lý hợp đồng chi tiết sẽ chuẩn không lệch số nhé.")


        # Thêm nút xóa toàn bộ sản phẩm trong đơn hàng
        remove_all_button = st.button("Xóa toàn bộ sản phẩm")
        if remove_all_button:
            st.session_state.order_items = []
            st.rerun()

        if len(st.session_state.order_items) == 0:
            st.warning("Đơn hàng trống. Vui lòng thêm sản phẩm.")

        st.write("---")

        # Tính tổng tiền đơn hàng        
        total_amount = order_items_df['subtotal'].sum() if len(order_items_df) > 0 else 0
        st.subheader(f"Tổng tiền: {total_amount:,} VNĐ")


        col1, col2 = st.columns(2)

        with col1:
            tien_coc = st.number_input("Tiền cọc", min_value=0, value=0, step=100000, format="%d")
            phi_van_chuyen = st.number_input("Phí vận chuyển", min_value=0, value=0, step=10000, format="%d")

        with col2:
            phi_cong_tho = st.number_input("Phí công thợ", min_value=0, value=0, step=100000, format="%d")
            phu_thu = st.number_input("Phụ thu", min_value=0, value=0, step=100000, format="%d")
        
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.session_state.thoi_gian_thuc_hien_don_hang = st.date_input("Thời gian yêu cầu thực hiện đơn hàng", format="DD/MM/YYYY", value=None)  
            if st.session_state.thoi_gian_thuc_hien_don_hang:
                # Chuyển đổi thành đối tượng datetime với thời gian mặc định là 00:00:00
                thoi_gian_datetime = datetime.datetime.combine(st.session_state.thoi_gian_thuc_hien_don_hang, datetime.time.min)
                # Chuyển đổi thành timestamp
                thoi_gian_thuc_hien_don_hang_timestamp = int(thoi_gian_datetime.timestamp())
                # Chuyển đổi thành chuỗi dạng "dd/mm/yyyy"
                thoi_gian_dd_mm_yyyy = st.session_state.thoi_gian_thuc_hien_don_hang.strftime("%d/%m/%Y")
            else:
                thoi_gian_thuc_hien_don_hang_timestamp = None
                thoi_gian_dd_mm_yyyy = None   


        with col4:
            so_luong_m2_yeu_cau_giu = st.text_input("Số m2 yêu cầu giữ & Yêu cầu khác từ khách", placeholder="Nhập dạng số vd: 26")
        
        uploaded_files = st.file_uploader("Upload SƠ ĐỒ NHÀ KHÁCH & hình ảnh mặt bằng (nếu đơn hoàn thiện)", accept_multiple_files=True)

        dia_chi_don_hang = st.text_input("Địa chỉ đơn hàng")
        ghi_chu_don_hang = st.text_area("Ghi chú", placeholder="Yêu cầu thêm của khách hàng, ghi chú,.... nhập vào đây!")
        

        


        # Thêm nút "Lưu đơn hàng"
        if st.button("Lưu đơn hàng"):
            # Tạo danh sách sản phẩm trong đơn hàng
            order_items = []
            for index, row in order_items_df.iterrows():
                product_id = row['product_id']
                quantity = int(row['quantity'])
                price = float(row['price'])
                note = unidecode.unidecode(row['note'])
                
                order_item = {
                    "fields": {
                        'Mã vật tư': product_id,
                        'Số lượng': quantity,
                        'Đơn giá': price,
                        'Ghi chú': note,
                    }
                }
                order_items.append(order_item)
            
            # Lấy thông tin khách hàng
            customer_name = unidecode.unidecode(customer_name)
            customer_phone = unidecode.unidecode(customer_phone)
            customer_ad_channel = unidecode.unidecode(customer_ad_channel)
            
            
            # Mã hóa các file về base64 và lưu vào mảng
            uploaded_files_data = []
            for uploaded_file in uploaded_files:
                file_content = uploaded_file.read() #đọc convert qua binary
                file_size = uploaded_file.size
                file_base64 = base64.b64encode(file_content).decode('utf-8')
                uploaded_files_data.append({
                    'file_name': uploaded_file.name,
                    'file_size': file_size,
                    'file_binary_content': file_base64
                })
                
                

                
                    
            # Tạo payload để gửi đi
            payload = {
                'order': {
                    'Thêm mới khách hàng?': is_new,
                    'customer_record_id': customer_record_id,
                    'customer_notes': customer_notes,
                    'Tên khách hàng': customer_name,
                    'Số điện thoại': customer_phone,
                    'ID khách hàng': str(customer_name) + " - " + str(customer_phone),
                    'Nguồn khách hàng': customer_ad_channel,
                    'Ghi chú': unidecode.unidecode(ghi_chu_don_hang),
                    'Tiền cọc': tien_coc,
                    'Phụ thu': phu_thu,
                    'Phí vận chuyển': phi_van_chuyen,
                    'Phí công thợ': phi_cong_tho,
                    'Hình thức đơn hàng': hinh_thuc_don_hang,
                    'Địa chỉ': dia_chi_don_hang,
                    'so_luong_m2_yeu_cau_giu': so_luong_m2_yeu_cau_giu,
                    'thoi_gian_thuc_hien_don_hang_timestamp': thoi_gian_thuc_hien_don_hang_timestamp,
                    'thoi_gian_thuc_hien_don_hang_date': thoi_gian_dd_mm_yyyy,
                    'hinh_thuc_thanh_toan': hinh_thuc_thanh_toan,
                    'tinh_trang_chot': tinh_trang_chot,
                    'attachments': uploaded_files_data,
                    'user_login': st.session_state.username,
                },
                'order_items': order_items,
                'flow_key': str(uuid.uuid4())  # Tạo flow_key duy nhất
            }
            
            # URL của API endpoint
            url = 'https://open-sg.larksuite.com/anycross/trigger/callback/MDkxMzQxNDMwOGE0ZGJlNDcyNGIyMGI0NWYwZTYwNDA1'
            
            
            # st.write(payload)
            
            # Gửi yêu cầu POST đến API endpoint với xác thực HTTP Basic Auth (nếu cần)
            response = requests.post(url, json=payload, auth=HTTPBasicAuth(user, password))
            # st.write(response)
            
            
            # Lấy mã trạng thái (status code) của phản hồi
            status_code = response.status_code

            # Lấy nội dung (content) của phản hồi
            response_content = response.text
            
            if status_code == 200:
                st.success("Đơn hàng đã được lưu và gửi đến webhook thành công!")
                st.markdown("Xem chi tiết đơn hàng tại [đây](https://qfnpn9xcbdi.sg.larksuite.com/wiki/DBnFww2deiGz67kRxEglSsjZgxg?table=tblZhHGDDX6sz9k1&view=vew49OBqZK).")
                st.info(f"Nội dung phản hồi: {response_content}")
            else:
                st.error("Có lỗi xảy ra khi lưu và gửi đơn hàng. Vui lòng thử lại.")
                st.error(f"Mã lỗi: {status_code}")
                st.error(f"Nội dung phản hồi: {response_content}")
        st.write("")
        with st.popover("Đăng xuất ứng dụng."):
            # Hiển thị các chức năng ở đây
            if st.button("Đăng xuất"):
                st.session_state.logged_in = False
                st.session_state.username = ''
                st.rerun()
login()