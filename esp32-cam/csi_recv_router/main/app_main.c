/* Get recv router csi

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"

#include "nvs_flash.h"

#include "esp_mac.h"
#include "rom/ets_sys.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_netif.h"
#include "esp_now.h"

#include "lwip/inet.h"
#include "lwip/netdb.h"
#include "lwip/sockets.h"
#include "ping/ping_sock.h"

#include "protocol_examples_common.h"

#if 1
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "nvs_flash.h"
#include "esp_mac.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_netif.h"
#include "esp_now.h"
#include "lwip/inet.h"
#include "lwip/netdb.h"
#include "lwip/sockets.h"
#include "ping/ping_sock.h"
#include "protocol_examples_common.h"

#define CONFIG_SEND_FREQUENCY      100

static const char *TAG = "csi_recv_router";

static void wifi_csi_rx_cb(void *ctx, wifi_csi_info_t *info){
    if (!info || !info->buf) {
        ESP_LOGW(TAG, "<%s> wifi_csi_cb", esp_err_to_name(ESP_ERR_INVALID_ARG));
        return;
    }

    if (memcmp(info->mac, ctx, 6)) {
        return;
    }

    static int s_count = 0;
    const wifi_pkt_rx_ctrl_t *rx_ctrl = &info->rx_ctrl;

    if (!s_count) {
        ESP_LOGI(TAG, "================ CSI RECV ================");
        ets_printf("type,seq,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,channel,secondary_channel,local_timestamp,ant,sig_len,rx_state,len,first_word,data\n");
    }

    /** Only LLTF sub-carriers are selected. */
    info->len = 128;

    printf("CSI_DATA,%d," MACSTR ",%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d",
            s_count++, MAC2STR(info->mac), rx_ctrl->rssi, rx_ctrl->rate, rx_ctrl->sig_mode,
            rx_ctrl->mcs, rx_ctrl->cwb, rx_ctrl->smoothing, rx_ctrl->not_sounding,
            rx_ctrl->aggregation, rx_ctrl->stbc, rx_ctrl->fec_coding, rx_ctrl->sgi,
            rx_ctrl->noise_floor, rx_ctrl->ampdu_cnt, rx_ctrl->channel, rx_ctrl->secondary_channel,
            rx_ctrl->timestamp, rx_ctrl->ant, rx_ctrl->sig_len, rx_ctrl->rx_state);

    printf(",%d,%d,\"[%d", info->len, info->first_word_invalid, info->buf[0]);

    for (int i = 1; i < info->len; i++) {
        printf(",%d", info->buf[i]);
    }

    printf("]\"\n");
}

static void wifi_csi_init(){
    /**
     * @brief In order to ensure the compatibility of routers, only LLTF sub-carriers are selected.
     */
    wifi_csi_config_t csi_config = {
        .lltf_en           = true,
        .htltf_en          = false,
        .stbc_htltf2_en    = false,
        .ltf_merge_en      = true,
        .channel_filter_en = true,
        .manu_scale        = true,
        .shift             = true,
    };

    static wifi_ap_record_t s_ap_info = {0};
    ESP_ERROR_CHECK(esp_wifi_sta_get_ap_info(&s_ap_info));
    ESP_ERROR_CHECK(esp_wifi_set_csi_config(&csi_config));
    ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(wifi_csi_rx_cb, s_ap_info.bssid));
    ESP_ERROR_CHECK(esp_wifi_set_csi(true));
}

static esp_err_t wifi_ping_router_start()
{
    static esp_ping_handle_t ping_handle = NULL;

    esp_ping_config_t ping_config = ESP_PING_DEFAULT_CONFIG();
    ping_config.count             = 0;
    ping_config.interval_ms       = 1000 / CONFIG_SEND_FREQUENCY;
    ping_config.task_stack_size   = 3072;
    ping_config.data_size         = 1;

    esp_netif_ip_info_t local_ip;
    esp_netif_get_ip_info(esp_netif_get_handle_from_ifkey("WIFI_STA_DEF"), &local_ip);
    ESP_LOGI(TAG, "got ip:" IPSTR ", gw: " IPSTR, IP2STR(&local_ip.ip), IP2STR(&local_ip.gw));
    ping_config.target_addr.u_addr.ip4.addr = ip4_addr_get_u32(&local_ip.gw);
    ping_config.target_addr.type = ESP_IPADDR_TYPE_V4;

    esp_ping_callbacks_t cbs = { 0 };
    esp_ping_new_session(&ping_config, &cbs, &ping_handle);
    esp_ping_start(ping_handle);

    return ESP_OK;
}

void app_main(){
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    /**
     * @brief This helper function configures Wi-Fi, as selected in menuconfig.
     *        Read "Establishing Wi-Fi Connection" section in esp-idf/examples/protocols/README.md
     *        for more information about this function.
     */
    ESP_ERROR_CHECK(example_connect());

    wifi_csi_init();
    wifi_ping_router_start();
}


#endif



#if 0

#define CONFIG_SEND_FREQUENCY      100
static const char *TAG = "csi_recv_router";

static void wifi_csi_rx_cb(void *ctx, wifi_csi_info_t *info){
    if (!info || !info->buf) {
        ESP_LOGW(TAG, "<%s> wifi_csi_cb", esp_err_to_name(ESP_ERR_INVALID_ARG));
        return;
    }

    if (memcmp(info->mac, ctx, 6)) {
        return;
    }

    static int s_count = 0;
    const wifi_pkt_rx_ctrl_t *rx_ctrl = &info->rx_ctrl;

    if (!s_count) {
        ESP_LOGI(TAG, "================ CSI RECV ================");
        ets_printf("type,seq,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,channel,secondary_channel,local_timestamp,ant,sig_len,rx_state,len,first_word,data\n");
    }

    /** Only LLTF sub-carriers are selected. */
    info->len = 128;
    vTaskDelay(pdMS_TO_TICKS(5000));
    printf("CSI_DATA,%d," MACSTR ",%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d",
            s_count++, MAC2STR(info->mac), rx_ctrl->rssi, rx_ctrl->rate, rx_ctrl->sig_mode,
            rx_ctrl->mcs, rx_ctrl->cwb, rx_ctrl->smoothing, rx_ctrl->not_sounding,
            rx_ctrl->aggregation, rx_ctrl->stbc, rx_ctrl->fec_coding, rx_ctrl->sgi,
            rx_ctrl->noise_floor, rx_ctrl->ampdu_cnt, rx_ctrl->channel, rx_ctrl->secondary_channel,
            rx_ctrl->timestamp, rx_ctrl->ant, rx_ctrl->sig_len, rx_ctrl->rx_state);

    printf(",%d,%d,\"[%d", info->len, info->first_word_invalid, info->buf[0]);

    for (int i = 1; i < info->len; i++) {
        printf(",%d", info->buf[i]);
    }
    vTaskDelay(pdMS_TO_TICKS(5000));
    printf("]\"\n");
}

// static void wifi_csi_init(){
//     /**
//      * @brief In order to ensure the compatibility of routers, only LLTF sub-carriers are selected.
//      */
//     wifi_csi_config_t csi_config = {
//         .lltf_en           = true,
//         .htltf_en          = false,
//         .stbc_htltf2_en    = false,
//         .ltf_merge_en      = true,
//         .channel_filter_en = true,
//         .manu_scale        = true,
//         .shift             = true,
//     };

//     // Wi-Fi가 이미 초기화되었다고 가정
//     // 따라서 Wi-Fi 관련 초기화 코드를 제거

//     // CSI 설정
//     static wifi_ap_record_t s_ap_info = {0};
//     esp_err_t err = esp_wifi_sta_get_ap_info(&s_ap_info);
//     if (err != ESP_OK) {
//         ESP_LOGE(TAG, "Failed to get AP info: %s", esp_err_to_name(err));
//         return;
//     }
//     ESP_ERROR_CHECK(esp_wifi_set_csi_config(&csi_config));
//     ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(wifi_csi_rx_cb, s_ap_info.bssid));
//     ESP_ERROR_CHECK(esp_wifi_set_csi(true));
//     vTaskDelay(pdMS_TO_TICKS(5000));
//     printf("4\n");
// }


static void wifi_csi_init(){
    /**
     * @brief In order to ensure the compatibility of routers, only LLTF sub-carriers are selected.
     */
    wifi_csi_config_t csi_config = {
        .lltf_en           = true,
        .htltf_en          = false,
        .stbc_htltf2_en    = false,
        .ltf_merge_en      = true,
        .channel_filter_en = true,
        .manu_scale        = true,
        .shift             = true,
    };

    static wifi_ap_record_t s_ap_info = {0};
    ESP_ERROR_CHECK(esp_wifi_sta_get_ap_info(&s_ap_info));
    ESP_ERROR_CHECK(esp_wifi_set_csi_config(&csi_config));
    ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(wifi_csi_rx_cb, s_ap_info.bssid));
    ESP_ERROR_CHECK(esp_wifi_set_csi(true));
    vTaskDelay(pdMS_TO_TICKS(5000));
    printf("4\n");

}

static esp_err_t wifi_ping_router_start(){
    static esp_ping_handle_t ping_handle = NULL;

    esp_ping_config_t ping_config = ESP_PING_DEFAULT_CONFIG();
    ping_config.count             = 0;
    ping_config.interval_ms       = 1000 / CONFIG_SEND_FREQUENCY;
    ping_config.task_stack_size   = 3072;
    ping_config.data_size         = 1;

    esp_netif_ip_info_t local_ip;
    esp_netif_get_ip_info(esp_netif_get_handle_from_ifkey("WIFI_STA_DEF"), &local_ip);
    ESP_LOGI(TAG, "got ip:" IPSTR ", gw: " IPSTR, IP2STR(&local_ip.ip), IP2STR(&local_ip.gw));
    ping_config.target_addr.u_addr.ip4.addr = ip4_addr_get_u32(&local_ip.gw);
    ping_config.target_addr.type = ESP_IPADDR_TYPE_V4;

    esp_ping_callbacks_t cbs = { 0 };
    esp_ping_new_session(&ping_config, &cbs, &ping_handle);
    esp_ping_start(ping_handle);
    vTaskDelay(pdMS_TO_TICKS(5000));
    printf("3\n");

    return ESP_OK;
}

// static EventGroupHandle_t s_wifi_event_group;
// #define WIFI_CONNECTED_BIT BIT0

// static void event_handler(void* arg, esp_event_base_t event_base,
//                           int32_t event_id, void* event_data)
// {
//     if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
//         esp_wifi_connect();
//     } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
//         ESP_LOGI(TAG, "Disconnected from Wi-Fi, attempting to reconnect...");
//         esp_wifi_connect();
//     } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
//         ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
//         ESP_LOGI(TAG, "Got IP:" IPSTR, IP2STR(&event->ip_info.ip));
//         xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
//     }
// }

// void app_main(){
//     // 기존 초기화 코드...
    
//     s_wifi_event_group = xEventGroupCreate();
    
//     ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
//                                                         ESP_EVENT_ANY_ID,
//                                                         &event_handler,
//                                                         NULL,
//                                                         NULL));
//     ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT,
//                                                         IP_EVENT_STA_GOT_IP,
//                                                         &event_handler,
//                                                         NULL,
//                                                         NULL));
    
//     ESP_ERROR_CHECK(example_connect());
    
//     // Wi-Fi 연결 대기
//     EventBits_t bits = xEventGroupWaitBits(s_wifi_event_group,
//                                            WIFI_CONNECTED_BIT,
//                                            pdFALSE,
//                                            pdFALSE,
//                                            portMAX_DELAY);
//     if (bits & WIFI_CONNECTED_BIT) {
//         ESP_LOGI(TAG, "Connected to AP");
//     } else {
//         ESP_LOGE(TAG, "Failed to connect to AP");
//         return;
//     }

//     wifi_csi_init();
//     printf("1\n");
//     vTaskDelay(pdMS_TO_TICKS(5000));
//     wifi_ping_router_start();
//     vTaskDelay(pdMS_TO_TICKS(5000));
//     printf("2\n");

//     // 메인 태스크가 종료되지 않도록 무한 루프 추가
//     while (1) {
//         vTaskDelay(pdMS_TO_TICKS(1000));
//     }
// }


void app_main(){
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    /**
     * @brief This helper function configures Wi-Fi, as selected in menuconfig.
     *        Read "Establishing Wi-Fi Connection" section in esp-idf/examples/protocols/README.md
     *        for more information about this function.
     */
    ESP_ERROR_CHECK(example_connect());
    // wifi_init();
    // printf("0\n");

    wifi_csi_init();
    printf("1\n");
    vTaskDelay(pdMS_TO_TICKS(5000));
    wifi_ping_router_start();
    vTaskDelay(pdMS_TO_TICKS(5000));
    printf("2\n");
}
#endif