#include <stdio.h> 
int arr[50005];
int n;
int ans=0;
int tar[50005];
int ar[50005];
void sorting(int idx, int prev,int pidx)
{
    if(idx > n){
        ar[pidx]=1;
        tar[ans++]=prev;
        return;
    }
    if(arr[idx]>prev && ar[idx]==0)
        sorting(idx+1,arr[idx],idx);
    else
        sorting(idx+1,prev,pidx);
}
int main()
{
    int  temp, i, j;
    scanf("%d",&n);
    for (i = 1; i <= n; i++)
    {
        scanf("%d", &arr[i]);
    }
    for(i = 1;i<=n;i++){
        sorting(1,-1,0);
    }
    for (i = 0; i < ans; i++)
    {
        printf("%d ", tar[i]);
    }
    printf("\n");
    return 0;
}