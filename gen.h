/* Released under AGPL v3 with exception for the OpenSSL library. See license.txt */

#ifndef __GEN_H__
#define __GEN_H__

#define RC_OK		0
#define RC_SHORTREAD	-1
#define RC_SHORTWRITE	-1
#define RC_TIMEOUT	-2
#define RC_CTRLC	-3
#define RC_INVAL	-4

#define RECV_BUFFER_SIZE (128 * 1024)

#define SPAM_FILE "/tmp/httping.dat"

#define MAX_SHOW_SUPPRESSION 3

#ifdef NO_SSL
	#define SSL	void
	#define SSL_CTX	void
	#define BIO	void
#endif

#define PI (4 * atan(1.0))
#define MY_DOUBLE_INF	999999999999999.9

#define min(x, y) ((x) < (y) ? (x) : (y))
#define max(x, y) ((x) > (y) ? (x) : (y))

#if USE_GETTEXT
#include <libintl.h>
#else
#define gettext(x) (x)
#endif

#ifdef __APPLE__
#include <AvailabilityMacros.h>
#if MAC_OS_X_VERSION_MIN_REQUIRED < 101100
#define NO_TFO
#endif
#endif

typedef struct
{
	double cur, min, avg, max, sd, med;
	int n;
	char valid, cur_valid;
	char calc_median;
	int median_size;
	double *median;
} stats_t;

int enc_b64(char *source, int source_lenght, char *target);

void init_statst(stats_t *data, char do_median);
void uninit_statst(stats_t *data);
void update_statst(stats_t *data, double in);
void reset_statst_cur(stats_t *data);
double calc_sd(stats_t *in);
double calc_median(const stats_t *in);

#endif
