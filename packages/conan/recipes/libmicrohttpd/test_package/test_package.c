/* Copyright (c) Contributors to the aswf-docker Project. All rights reserved. */
/* SPDX-License-Identifier: Apache-2.0 */

#include <microhttpd.h>
#include <stdio.h>

static enum MHD_Result handler(void *cls, struct MHD_Connection *connection,
                                const char *url, const char *method,
                                const char *version, const char *upload_data,
                                size_t *upload_data_size, void **ptr) {
    (void)cls; (void)connection; (void)url; (void)method;
    (void)version; (void)upload_data; (void)upload_data_size; (void)ptr;
    return MHD_NO;
}

int main(void) {
    struct MHD_Daemon *daemon = MHD_start_daemon(
        MHD_USE_INTERNAL_POLLING_THREAD,
        0,       /* port 0 = OS assigns a free port */
        NULL, NULL,
        &handler, NULL,
        MHD_OPTION_END);
    if (daemon == NULL) {
        fprintf(stderr, "MHD_start_daemon failed\n");
        return 1;
    }
    MHD_stop_daemon(daemon);
    printf("libmicrohttpd OK (version %s)\n", MHD_get_version());
    return 0;
}
